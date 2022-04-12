import struct


def decode(data, tag=None, reverse=False):
    if tag in DECODE_FUNC_FULL:
        decode_func = DECODE_FUNC_FULL[tag]
    else:
        decode_func = DECODE_FUNC_FIRST[tag[0]]
    return decode_func(data, reverse=reverse)


def decode_struct(data, reverse=False):
    if reverse:
        ret_data = bytes()
        for dat in data:
            tag = dat[0]
            value = decode(dat[1], tag=tag, reverse=reverse)
            length = struct.pack('>I', len(value))
            ret_data = ret_data + tag.encode('utf-8') + length + value
        return ret_data

    ret = []
    i = 0
    while i < len(data):
        tag = data[i:i + 4].decode('ascii')
        length = struct.unpack('>I', data[i + 4:i + 8])[0]
        value = data[i + 8:i + 8 + length]
        value = decode(value, tag=tag)
        ret.append((tag, value))
        i += 8 + length
    return ret


def decode_unicode(data, reverse=False):
    if reverse:
        return data.encode('utf-16-be')
    return data.decode('utf-16-be')


def decode_unsigned(data, reverse=False):
    if reverse:
        return struct.pack('>I', data)
    return struct.unpack('>I', data)[0]


def noop(data, reverse=False):
    if reverse and isinstance(data, str):
        return data.encode('utf-8')
    else:
        return data


DECODE_FUNC_FULL = {
    None: decode_struct,
    'vrsn': decode_unicode,
    'sbav': noop,
}

DECODE_FUNC_FIRST = {
    'o': decode_struct,
    't': decode_unicode,
    'p': decode_unicode,
    'u': decode_unsigned,
    'b': noop,
}
