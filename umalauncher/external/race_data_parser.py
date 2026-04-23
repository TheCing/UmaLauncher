import base64
import gzip
import struct
import sys
import util
sys.path.append(util.get_asset('external'))

import race_data_pb2


def deserialize_header(b: bytearray) -> (race_data_pb2.RaceSimulateHeaderData, int):
    header = race_data_pb2.RaceSimulateHeaderData()
    header.max_length, header.version = struct.unpack_from('<ii', b, offset=0)
    return header, 4 + header.max_length


def deserialize_horse_frame(b: bytearray, offset: int) -> race_data_pb2.RaceSimulateHorseFrameData:
    horse_frame = race_data_pb2.RaceSimulateHorseFrameData()
    (distance, lane_position, speed, hp, temptation_mode,
     block_front_horse_index) = struct.unpack_from('<fHHHbb', b, offset=offset)
    horse_frame.distance = distance
    horse_frame.lane_position = lane_position
    horse_frame.speed = speed
    horse_frame.hp = hp
    _set_enum_safe(horse_frame, 'temptation_mode', temptation_mode)
    horse_frame.block_front_horse_index = block_front_horse_index
    return horse_frame


def deserialize_frame(b: bytearray, offset: int, horse_num: int,
                      horse_frame_size: int) -> race_data_pb2.RaceSimulateFrameData:
    frame = race_data_pb2.RaceSimulateFrameData()
    frame.time = struct.unpack_from('<f', b, offset=offset)[0]
    offset += 4
    for i in range(horse_num):
        frame.horse_frame.append(deserialize_horse_frame(b, offset))
        offset += horse_frame_size
    return frame


def _set_enum_safe(msg, field, value):
    """Assign an enum field tolerant of unknown values from newer game versions."""
    try:
        setattr(msg, field, value)
    except ValueError:
        pass  # unknown enum value — leave unset


def deserialize_horse_result(b: bytearray, offset: int) -> race_data_pb2.RaceSimulateHorseResultData:
    horse_result = race_data_pb2.RaceSimulateHorseResultData()
    (finish_order, finish_time, finish_diff_time, start_delay_time,
     guts_order, wiz_order, last_spurt_start_distance,
     running_style, defeat,
     finish_time_raw) = struct.unpack_from('<ifffBBfBif', b, offset)
    horse_result.finish_order = finish_order
    horse_result.finish_time = finish_time
    horse_result.finish_diff_time = finish_diff_time
    horse_result.start_delay_time = start_delay_time
    horse_result.guts_order = guts_order
    horse_result.wiz_order = wiz_order
    horse_result.last_spurt_start_distance = last_spurt_start_distance
    _set_enum_safe(horse_result, 'running_style', running_style)
    horse_result.defeat = defeat
    horse_result.finish_time_raw = finish_time_raw
    return horse_result


def deserialize_event(b: bytearray, offset: int) -> race_data_pb2.RaceSimulateEventData:
    event = race_data_pb2.RaceSimulateEventData()
    fmt = '<fbb'
    (frame_time, event_type, param_count) = struct.unpack_from(fmt, b, offset)
    event.frame_time = frame_time
    _set_enum_safe(event, 'type', event_type)
    event.param_count = param_count
    offset += struct.calcsize(fmt)
    for i in range(event.param_count):
        event.param.append(struct.unpack_from('<i', b, offset)[0])
        offset += 4
    return event


def deserialize(b: bytearray) -> race_data_pb2.RaceSimulateData:
    data = race_data_pb2.RaceSimulateData()

    header, offset = deserialize_header(b)
    data.header.CopyFrom(header)
    version = header.version

    # Version 100000004+ removed the single horse_result_size field and
    # replaced it with a per-horse array before the results. Each horse's
    # block is 31 bytes (standard result) + 8 bytes (unknown+skill_count)
    # + 5*N bytes (N skill activations: skill_id int32 + activated byte).
    v4_plus = version >= 100000004

    if v4_plus:
        data.distance_diff_max, data.horse_num, data.horse_frame_size = \
            struct.unpack_from('<fii', b, offset)
        data.horse_result_size = 0  # variable per-horse in v4+
        offset += 12
    else:
        data.distance_diff_max, data.horse_num, data.horse_frame_size, data.horse_result_size = \
            struct.unpack_from('<fiii', b, offset)
        offset += 16

    data.__padding_size_1 = struct.unpack_from('<i', b, offset)[0]
    offset += 4 + data.__padding_size_1

    fmt = '<ii'
    data.frame_count, data.frame_size = struct.unpack_from(fmt, b, offset)
    offset += struct.calcsize(fmt)

    for i in range(data.frame_count):
        data.frame.append(deserialize_frame(b, offset, data.horse_num, data.horse_frame_size))
        offset += data.frame_size

    data.__padding_size_2 = struct.unpack_from('<i', b, offset)[0]
    offset += 4 + data.__padding_size_2

    # v4+: read per-horse result sizes, then each horse_result uses its own size
    if v4_plus:
        horse_result_sizes = list(
            struct.unpack_from(f'<{data.horse_num}i', b, offset)
        )
        offset += data.horse_num * 4
    else:
        horse_result_sizes = [data.horse_result_size] * data.horse_num

    for i in range(data.horse_num):
        data.horse_result.append(deserialize_horse_result(b, offset))
        offset += horse_result_sizes[i]

    data.__padding_size_3 = struct.unpack_from('<i', b, offset)[0]
    offset += 4 + data.__padding_size_3

    data.event_count = struct.unpack_from('<i', b, offset)[0]
    offset += 4

    for i in range(data.event_count):
        event_wrapper = race_data_pb2.RaceSimulateData.EventDataWrapper()
        event_wrapper.event_size = struct.unpack_from('<h', b, offset)[0]
        offset += 2
        event_wrapper.event.CopyFrom(deserialize_event(b, offset))
        offset += event_wrapper.event_size
        data.event.append(event_wrapper)

    return data

def parse(race_scenario):
    return deserialize(gzip.decompress(base64.b64decode(race_scenario)))

def main():
    b = input('Please paste content of field "race_scenario" here: ').strip('"')
    b = gzip.decompress(base64.b64decode(b))
    print(deserialize(b))


if __name__ == '__main__':
    main()
