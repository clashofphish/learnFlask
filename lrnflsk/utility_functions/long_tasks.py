import time


def simple_long_task(duration: str, message):
    duration = int(duration)
    for i in range(duration):
        print("Working... {}/{}".format(i + 1, duration))
        time.sleep(2)
        if i == duration - 1:
            print('Completed work on {}'.format(duration))

    mess_del = message.delete()
    if mess_del['ResponseMetadata']['HTTPStatusCode'] == 200:
        return 'Message deleted for duration: {}'.format(duration)
    else:
        return 'Message deletion failed for duration: {}'.format(duration)


def broken_long_task(duration: str, message):
    duration = int(duration)
    for i in range(duration):
        if i + 1 > 5:
            raise Exception('Bugger off no numbers above 5')
        else:
            print("Working... {}/{}".format(i + 1, duration))
        time.sleep(2)

    mess_del = message.delete()
    if mess_del['ResponseMetadata']['HTTPStatusCode'] == 200:
        return 'Message deleted for duration: {}'.format(duration)
    else:
        return 'Message deletion failed for duration: {}'.format(duration)




