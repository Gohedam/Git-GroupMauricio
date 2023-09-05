import requests
import json

access_token = 'YTA3ODk5MzktMjU4YS00Y2U1LThlZGYtOTljMjMzMmQ4ZjBlMDQ1ZmY3NTItYzc0_P0A1_ff79c397-9d79-44f7-8296-8858b58f5ba8'
base_url = 'https://api.ciscospark.com/v1'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

room_name = 'Devnet-GroupMauricio'
group_members = ['fernando.urena@sistemas.edu.bo','mghpugna@hotmail.com','marisarpa1001@gmail.com','rc4rlos@gmail.com','rocher.rhg.91@gmail.com', ...]


rooms_url = f'{base_url}/rooms'
response = requests.get(rooms_url, headers=headers)
rooms = response.json()['items']
room_id = None
for room in rooms:
    if room['title'] == room_name:
        room_id = room['id']
        break

if room_id:
    print(f'Room "{room_name}" already exists with ID: {room_id}')
    memberships_url = f'{base_url}/memberships?roomId={room_id}'
    response = requests.get(memberships_url, headers=headers)
    memberships = response.json()['items']
    print('Members:')
    for membership in memberships:
        print(f'- {membership["personEmail"]}')
else:
    create_room_url = f'{base_url}/rooms'
    data = {'title': room_name}
    response = requests.post(create_room_url, headers=headers, data=json.dumps(data))
    room_id = response.json()['id']
    print(f'Created new room "{room_name}" with ID: {room_id}')

    for member in group_members:
        create_membership_url = f'{base_url}/memberships'
        data = {'roomId': room_id, 'personEmail': member}
        response = requests.post(create_membership_url, headers=headers, data=json.dumps(data))

message_url = f'{base_url}/messages'
data = {
    'roomId': room_id,
    'text': 'Docker Hub container path: https://hub.docker.com/repository/docker/mherbas/docker-groupmauricio/general'
}
response = requests.post(message_url, headers=headers, data=json.dumps(data))