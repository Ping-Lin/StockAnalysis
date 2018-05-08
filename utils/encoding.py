def encoding_transform(data, enc='latin1', type_encode='strict', dec='big5'):
    try:
        data = str(data).encode(enc, type_encode).decode(dec)
    except UnicodeEncodeError as e:
        # print("encode error: {}, {}...", e, data[0:30])
        pass
    except UnicodeDecodeError as e:
        # print("decode error: {}, {}...", e, data[0:30])
        pass
    except UnicodeError as e:
        # print("unicode error: {}, {}...", e, data[0:30])
        pass
    return data
