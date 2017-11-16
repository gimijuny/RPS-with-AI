#두번 가위 바위보
#둘 다 같은것만 냄
import random

pl_f = '';
pl_s = '';
com_f = '';
com_s = '';

out = True;

score = 0;
win = 0;
lose = 0;

while out :
	# 플레이어 첫번째 값 입력, 출력
	while True :
		pl_f = input("첫번째(가위, 바위, 보 중 하나를 입력해주세요.)>>")
		if pl_f == '가위' :
			print("플레이어_첫번째: 가위")
			break;
		elif pl_f == '바위' :
			print("플레이어_첫번째: 바위")
			break;
		elif pl_f == '보':
			print("플레이어_첫번째: 보")
			break;
		else:
			print("잘못된 값을 입력했습니다.")

	# 컴퓨터 값 출력
	com_f = random.randint(1, 3)
	if com_f == 1 :
		print("컴퓨터_첫번째: 가위")
		com_s = 1
	elif com_f == 2 :
		print("컴퓨터_첫번째: 바위")
		com_s = 2
	else:  # com_f == 3
		print("컴퓨터_첫번째: 보")
		com_s = 3
	
	#승패판정, 점수 계산
	while True :
		pl_s = input("두번째(가위, 바위, 보 중 하나를 입력해주세요.)>>")

		if pl_s == '가위' : #가위
			print("플레이어_두번째: 가위")
			if com_s == 3 : #보
				print("컴퓨터_두번째: 보")
				print("당신이 이겼습니다!")
				if pl_s == pl_f :
					score += 2
					win += 1
					print("2점 획득!")
				else :
					score += 1
					win += 1
					print("1점 획득!")
				break;
			elif com_s == 2 : #바위
				print("컴퓨터_두번째: 바위")
				print("당신이 졌습니다...")
				lose += 1
				break;
			else: #가위
				print("컴퓨터_두번째: 가위")
				print("비겼습니다.")

		elif pl_s == '바위' : #바위
			print("플레이어_두번째: 바위")
			if com_s == 1 : #가위
				print("컴퓨터_두번째: 가위")
				print("당신이 이겼습니다!")
				if pl_s == pl_f :
					score += 2
					win += 1
					print("2점 획득!")
				else :
					score += 1
					win += 1
					print("1점 획득!")
				break;
			elif com_s == 3 : #보
				print("컴퓨터_두번째: 보")
				print("당신이 졌습니다...")
				lose += 1
				break;
			else: #바위
				print("컴퓨터_두번째: 바위")
				print("비겼습니다.")

		elif pl_s == '보': #보
			print("플레이어_두번째: 보")
			if com_s == 2 : #바위
				print("컴퓨터_두번째: 바위")
				print("당신이 이겼습니다!")
				if pl_s == pl_f :
					score += 2
					win += 1
					print("2점 획득!")
				else :
					score += 1
					win += 1
					print("1점 획득!")
				break;
			elif com_s == 1 : #가위
				print("컴퓨터_두번째: 가위")
				print("당신이 졌습니다...")
				lose += 1
				break;
			else: #보
				print("컴퓨터_두번째: 보")
				print("비겼습니다.")
		else :
			print("잘못된 값을 입력했습니다.")

	print("")	
	out = input("끝내시겠습니까? 예:1 아니오:아무 키나 누르십시오. >>")
	print("")

	if out == '1' :
		print("승리: %s번, 패배: %s번" %(win, lose) )
		print("점수: %s점" %score)
		break;