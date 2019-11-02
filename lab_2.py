MAX_ITERATIONS = 10000
MATRIX_SIZE = 10
START_COIN_COUNT = 1e6
COIN_COUNT_FOR_ONE_GIVE = 1000

class Country:
    def __init__(self, coord_1, coord_2, name, list_cities=[]):
        self.name = name
        self.coord_c_1 = tuple(coord_1)
        self.coord_c_2 = tuple(coord_2)
        self.list_cities = list_cities


    def __str__(self):
        return '{} - A({}) B({}); count cities - {}'.format(self.name, self.coord_c_1, self.coord_c_2,
                                                            len(self.list_cities))

    def country_finish(self):
        for city in self.list_cities:
            if not city.finish_exchange:
                return False

class City:
    def __init__(self, x, y, all_count_countries, index):
        # print('all_count_countries', all_count_countries)
        self.coord_city_x = x
        self.coord_city_y = y
        self.finish_exchange = False
        self.siblings = None
        self.all_count_countries = all_count_countries
        self.other_money_country = [0] * all_count_countries
        self.all_money = [0] * all_count_countries
        self.all_money[index] = START_COIN_COUNT

    def __str__(self):
        return 'city {} {}'.format(self.coord_city_x, self.coord_city_y)

    def print_info(self):
        print(self.other_money_country)
        print('----------')
        print(self.all_money)

    def give_money_siblings(self):
        count_not_empty_items = []
        for price in self.other_money_country:
            # print(price)
            if price > 0:
                count_not_empty_items.append(True)

        if len(count_not_empty_items) == self.all_count_countries:
            self.finish_exchange = True

        for index, coin_for_other in enumerate(self.other_money_country):
            if coin_for_other >= COIN_COUNT_FOR_ONE_GIVE:
                share = coin_for_other // COIN_COUNT_FOR_ONE_GIVE
                for city in self.siblings:
                    city.all_money[index] += share
                    self.other_money_country[index] -= share

    def end_day(self):
        for i in range(self.all_count_countries):
            self.other_money_country[i] += self.all_money[i]
            self.all_money[i] = 0


def main():
    # count_coutry = int(input('Count country >>> '))
    while True:
        try:
            count_coutry = int(input('Count country >>> '))
            break
        except ValueError as e:
            print('invalid number')
    # if not isinstance(count_coutry, int):
    #     print("enter number")

    total_count = count_coutry
    all_countries = []
    # index = 0
    try:

        while count_coutry:
            name = input('Enter name country >>> ')
            loop = True
            while loop:

                try:
                    county_coords_1 = tuple(map(int, input('Enter first coordinate for country >>>').split(' ')))
                    county_coords_2 = tuple(map(int, input('Enter second coordinate for country >>>').split(' ')))
                    # print('county_coords_1', county_coords_1, 'county_coords_2', county_coords_2)
                    if not (all(1 <= x <= MATRIX_SIZE for x in county_coords_1) and all(1 <= x <= MATRIX_SIZE for x in county_coords_2)):
                        raise ValueError
                    else:
                        loop = False
                except ValueError as e:
                    print('invalid range (1-10)')
            cities_list = []
            for y in range(county_coords_1[1], county_coords_2[1] + 1):
                for x in range(county_coords_1[0], county_coords_2[0] + 1):
                    new_city = City(x=x, y=y, all_count_countries=total_count, index=total_count - count_coutry)
                    # new_city.print_info()
                    cities_list.append(new_city)

            new_country = Country(name=name,
                                  coord_1=county_coords_1,
                                  coord_2=county_coords_2,
                                  list_cities=cities_list)
            all_countries.append(new_country)
            # index += 1
            count_coutry -= 1

        else:
            print('generate county with cities end!!!!!!')

            def build_all_matrix(list_country):
                # xs = []
                # ys = []
                # for c in list_country:
                #     xs.extend((c.coord_c_1[0], c.coord_c_2[0]))
                #     ys.extend((c.coord_c_1[1], c.coord_c_2[1]))
                # min_x = min(xs)
                # max_x = max(xs)
                # min_y = min(ys)
                # max_y = max(ys)
                # y_range = range(max_y - min_y + 1)
                # x_range = range(max_x - min_x + 1)
                matrix = []
                for _ in range(MATRIX_SIZE):
                    sub_list = []
                    for _ in range(MATRIX_SIZE):
                        sub_list.append(None)
                    matrix.append(sub_list)
                return matrix
                # return [[None for j in y_range] for i in x_range]

            all_matrix = build_all_matrix(list_country=all_countries)
        # print( all_matrix)
        for country in all_countries:
            # print (country)
            for city in country.list_cities:
                all_matrix[city.coord_city_x - 1][city.coord_city_y - 1] = city

        width = MATRIX_SIZE
        heigth = MATRIX_SIZE

        for x in range(width):
            for y in range(heigth):
                city = all_matrix[x][y]
                if city is not None:
                    siblings = []
                    if x + 1 <= width - 1 and all_matrix[x + 1][y]:
                        siblings.append(all_matrix[x + 1][y])
                    if x - 1 >= 0 and all_matrix[x - 1][y]:
                        siblings.append(all_matrix[x - 1][y])
                    if y + 1 <= heigth - 1 and all_matrix[x][y + 1]:
                        siblings.append(all_matrix[x][y + 1])
                    if y - 1 >= 0 and all_matrix[x][y - 1]:
                        siblings.append(all_matrix[x][y - 1])
                    city.siblings = siblings

        result = {}
        days = 0
        while True:
            for country_1 in all_countries:
                for city in country_1.list_cities:
                    city.give_money_siblings()
                if country_1.country_finish():
                    if country_1.name not in result:
                        result[country_1.name] = days - 1
            if all(map(lambda x: x.country_finish(), all_countries)):
                break

            for country in all_countries:
                for city in country.list_cities:
                    city.end_day()
            days += 1
            if days == MAX_ITERATIONS:
                print("Can`t calc")
                break
        if days < MAX_ITERATIONS:
            for key in result:
                print('{} - {}'.format(key, result[key]))


    except Exception as e:
        pass



if __name__ == '__main__':
    main()
