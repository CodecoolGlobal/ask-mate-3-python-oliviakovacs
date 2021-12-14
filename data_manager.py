import connection

def sort(filename, type="submission_time", order="descending"):
    data = connection.get_data(filename)
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[i][type].isnumeric() and int(data[i][type]) > int(data[j][type]):
                data[i], data[j] = data[j], data[i]
            elif data[i][type] > data[j][type]:
                data[i], data[j] = data[j], data[i]
    if order == "descending":
        return data
    return data[::-1]