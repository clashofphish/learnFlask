import time

import lrnflsk.utility_functions.sqs_utilities as sqs_ut


def simple_long_task(queue_resource):
    while True:
        start = time.time()
        messages = sqs_ut.sqs_pull_messages(queue_resource, max_messages=5)
        end = time.time()
        print('Time wait for queue response {}'.format(end - start))
        for message in messages:
            duration = int(message.body)
            # In actual code would perform a message validation
            for i in range(duration):
                print("Working... {}/{}".format(i + 1, duration))
                time.sleep(2)
                if i == duration - 1:
                    print('Completed work on {}'.format(duration))

            mess_del = message.delete()
            if mess_del['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('Message deleted for duration: {}'.format(duration))
            else:
                print('Message deletion failed for duration: {}'.format(duration))


def broken_long_task(queue_resource):
    messages = sqs_ut.sqs_pull_messages(queue_resource, max_messages=5)
    for message in messages:
        duration = int(message.body)
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




