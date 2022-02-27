import json

ONOFF = "OFF"

async def _check_if_user_vip(user,db):
	state = False
	for i in db:
		test = int(i)
		if int(i) == user:
			state = True
		else:
			pass
	return state

async def _react(reaction,message):
	print("Adding reaction...")
	await message.add_reaction(reaction)
	print("Addded.")

async def main(message):
	if ONOFF == "ON":
		db = json.load(open("vip.json"))
		state = await _check_if_user_vip(user=message.author.id,db=db)
		if state == True:
			print("User in the vip db, reacting...")
			await _react(db[str(message.author.id)],message)
		else:
			print("User is not in vip db")
	elif ONOFF == "OFF":
		print("Vip system disabled")
	else:
		print("Unknown state, vip disabled.")