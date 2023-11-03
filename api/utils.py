from .models import Tour, TourURL, TourOperator


def load_data_from_dataframe(data):
    print("DATA =", data)
    for idx, d in enumerate(data):
        # todo, add category
        tour_operator = TourOperator.objects.filter(name=d['operator']).first()
        if not tour_operator:
            print("Tour Operator create = ", d['operator'])
            tour_operator = TourOperator.objects.create(name=d['operator'])
        try:
            tour, created = Tour.objects.update_or_create(
                tour_operator=tour_operator,
                country=d['country'],
                city=d['city'],
                rating=float(d['rating']) if d['rating'] else None,
                state=d['state'],
                email=d['email'],
                website=d['website'],
                # category=d['category'],
                rating_override=True if d['rating'] else False,
                defaults={'date_created': d['date_created']},
            )
        except:
            try:
                tour = Tour.objects.filter(
                    tour_operator=tour_operator,
                    country=d['country'],
                    city=d['city'],
                    rating=float(d['rating']) if d['rating'] else None,
                    state=d['state'],
                    email=d['email'],
                    website=d['website'],
                    # category=d['category'],
                    rating_override=True if d['rating'] else False,
                    date_created=d['date_created']
                ).first()
            except:
                continue
        print(tour)
        print(d['stream_data'])
        for s in d['stream_data']:
            TourURL.objects.update_or_create(
                tour=tour,
                url=s['url'],  # Utilizza l'URL come campo univoco per identificare un TourURL specifico
                defaults={'stream': s['stream']}
            )
        print('updated stream')
        print(len(data))