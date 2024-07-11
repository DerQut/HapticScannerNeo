def missingXMLFallback():
    f = open("config.xml", "w+")
    f.write("""<data>
        <config>
            <savedir>C:/PomiaryHaptyczne/</savedir>
            <host>192.168.1.103</host>
            <port>8881</port>
            <createnewfolder>1</createnewfolder>
            <autosave>1</autosave>
        </config>

        <pid>
            <setpoint>31882</setpoint>
            <setpointlowerlimit>-10</setpointlowerlimit>
            <setpointupperlimit>10</setpointupperlimit>
            <isonline>1</isonline>
            <gain name="proportional">
                <value>7208</value>
                <upperlimit>1.0</upperlimit>
                <lowerlimit>0.0</lowerlimit>
            </gain>
            <gain name="integral">
                <value>57539</value>
                <upperlimit>2.0</upperlimit>
                <lowerlimit>-3.0</lowerlimit>
            </gain>
            <gain name="differential">
                <value>6917</value>
                <upperlimit>10.0</upperlimit>
                <lowerlimit>1.0</lowerlimit>
            </gain>
        </pid>

        <channels>
            <channel id="1">
                <enabled>1</enabled>
                <name>Channel 1</name>
            </channel>
            <channel id="2">
                <enabled>1</enabled>
                <name>Channel 2</name>
            </channel>
            <channel id="3">
                <enabled>1</enabled>
                <name>Channel 3</name>
            </channel>
            <channel id="4">
                <enabled>1</enabled>
                <name>Channel 4</name>
            </channel>
            <channel id="5">
                <enabled>1</enabled>
                <name>Channel 5</name>
            </channel>
            <channel id="6">
                <enabled>1</enabled>
                <name>Channel 6</name>
            </channel>
            <channel id="7">
                <enabled>1</enabled>
                <name>Channel 7</name>
            </channel>
            <channel id="8">
                <enabled>1</enabled>
                <name>Channel 8</name>
            </channel>
            <channel id="9">
                <enabled>1</enabled>
                <name>Channel 9</name>
            </channel>
            <channel id="10">
                <enabled>1</enabled>
                <name>Channel 10</name>
            </channel>
        </channels>

    </data>""")
    f.close()