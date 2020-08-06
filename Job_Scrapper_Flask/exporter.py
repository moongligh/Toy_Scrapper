import csv

def save_to_csv(jobs):
    file = open('jobs.csv', mode='w', encoding='utf-8') # 목표 파일,환경 설정
    writer =csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link'])   # csv파일의 첫줄을 doc형식과 일치시켜 작성한다.

    for job in jobs:
        writer.writerow(list(job.values())) # job의 doc의 value값을 list로 정렬하여 작성하기

    return