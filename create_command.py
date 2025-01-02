command = "run opcua client where \n\turl=opc.tcp://10.0.0.228:4840/freeopcua/server/ \n\tand frequency=25 \n\tand dbms=nov \n\tand table=%s"
data = {
    2: "table_1",
    3: "table_2",
    4: "table_3",
    5: "table_4",
    6: "table_5"
}



for table in data:
    my_cmd = f"<{command % data[table]}"
    for point in list(range(2, 104)):
        my_cmd += f'\n\tand node = "ns={table};i={point}"'
    print(my_cmd + ">")



# run opcua client where url =opc.tcp://10.0.0.228:4840/freeopcua/server/ and node = "ns=2;i=2" and frequency=25 and dbms=nov and table=table_2

