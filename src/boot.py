import network
import config
import esp
import gc


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():

        print('connecting to network...')

        wlan.connect(config.ESSID, config.PASSWORD)

        while not wlan.isconnected():
            pass

    print('network config:', wlan.ifconfig())


esp.osdebug(None)
gc.collect()
do_connect()
