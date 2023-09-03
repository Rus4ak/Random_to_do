import argparse
from api import ApiCall
from db import RandomToDoDB

def main():
    parser = argparse.ArgumentParser(description='Manage random activities')
    subparsers = parser.add_subparsers(dest='subcommand', help='Available subcommands')

    new_parser = subparsers.add_parser('new', help='Get and save a random activity based on filters')
    new_parser.add_argument('--type', help='Filter by activity type')
    new_parser.add_argument('--participants', type=int, help='Filter by number of participants')
    new_parser.add_argument('--price_min', type=float, help='Minimum price filter')
    new_parser.add_argument('--price_max', type=float, help='Maximum price filter')
    new_parser.add_argument('--accessibility_min', type=float, help='Minimum accessibility filter')
    new_parser.add_argument('--accessibility_max', type=float, help='Maximum accessibility filter')

    list_parser = subparsers.add_parser('list', help='List of 5 recent activities')

    args = parser.parse_args()
    api_call = ApiCall()
    db = RandomToDoDB()

    if args.subcommand == 'new':
        kwargs = {
            'type': args.type,
            'participants': args.participants,
            'minprice': args.price_min,
            'maxprice': args.price_max,
            'minaccessibility': args.accessibility_min,
            'maxaccessibility': args.accessibility_max
        }

        result = api_call.new_activity(**kwargs)
        print('New activity created successfully ')

        for key, value in result.items():
            print(f'\t {key} - {value}')

    elif args.subcommand == 'list':
        result = db.show_activities()
        i = 1

        for activities in result:
            print(f'''{i}. activity - {activities[0]}
                    \rtype - {activities[1]}
                    \rparticipants - {activities[2]}
                    \rprice - {activities[3]}
                    \rlink - {activities[4]}
                    \rkey - {activities[5]}
                    \raccessibility {activities[6]}\n ''')
            
            i += 1

    else:
        print('Invalid subcommand')

if __name__ == '__main__':
    main()
