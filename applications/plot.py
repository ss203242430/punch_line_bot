import matplotlib.pyplot as plt 
import datetime

domain = 'pieta.myddns.me:3001'

def learn_punch_report_plot(learn_punch_list):
    x = []
    x_label = []
    y = []

    count = 0
    for learn_punch in learn_punch_list:
        if learn_punch.clock_out:
            count += 1
            x.append(count)
            date = learn_punch.clock_in.strftime("%Y%m%d")
            x_label.append(date)
            total_seconds = (learn_punch.clock_out - learn_punch.clock_in).total_seconds()
            y.append(total_seconds)
    if count > 6:
        x_label[1:-1] = ''

    plt.plot(x, y, marker="o")
    plt.xticks(x, x_label)
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    plt.savefig(f'static/plot/temp/learn_punch_report_{timestamp}.png')
    plt.close()
    plt_img_url = f'https://{domain}/static/plot/temp/learn_punch_report_{timestamp}.png'
    return plt_img_url

def learn_punch_week_report_plot(learn_punch_list, week_start):
    week_day = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'] 

    x = [1, 2, 3, 4, 5, 6, 7]
    y = []

    session_start = week_start
    session_end = session_start + datetime.timedelta(days=1)

    result = {
        'MON': datetime.timedelta(),
        'TUE': datetime.timedelta(),
        'WED': datetime.timedelta(),
        'THU': datetime.timedelta(),
        'FRI': datetime.timedelta(),
        'SAT': datetime.timedelta(),
        'SUN': datetime.timedelta()
    }
    week_day_index = 0
    for learn_punch in learn_punch_list:
        while learn_punch.clock_in > session_end:
            session_start = session_end
            session_end = session_start + datetime.timedelta(days=1)
            week_day_index += 1
        if learn_punch.clock_out:
            result[week_day[week_day_index]] += learn_punch.clock_out - learn_punch.clock_in

    y.append(result['MON'].total_seconds())
    y.append(result['TUE'].total_seconds())
    y.append(result['WED'].total_seconds())
    y.append(result['THU'].total_seconds())
    y.append(result['FRI'].total_seconds())
    y.append(result['SAT'].total_seconds())
    y.append(result['SUN'].total_seconds())

    plt.plot(x, y, marker="o")
    plt.xticks(x, week_day)
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    plt.savefig(f'static/plot/temp/learn_punch_week_report_{timestamp}.png')
    plt.close()
    plt_img_url = f'https://{domain}/static/plot/temp/learn_punch_week_report_{timestamp}.png'
    return plt_img_url