class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration,
                 distance,
                 speed,
                 calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

    def __init__(self,
                 action: int,  # Количество действия.
                 duration: float,  # Время в часах.
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__str__(), self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        training_duration = self.duration * self.H_IN_MIN
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * training_duration)

    # Новый метод базового класса.
    def __str__(self):
        return f'{self.__class__.__name__}'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.349.252"""
    CALORIES_WEIGHT_MULTIPLIER_1 = 0.035
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.029
    KMH_IN_MS = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed() * self.KMH_IN_MS
        training_duration = self.duration * self.H_IN_MIN
        sportsman_height = self.height / self.SM_IN_M
        return ((self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight +
                (mean_speed ** 2 / sportsman_height) *
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight) *
                training_duration)

    # Новый метод базового класса.
    def __str__(self):
        return f'{self.__class__.__name__}'


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_MEAN_SPEED_TWO = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM /
                self.duration)

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return ((mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MEAN_SPEED_TWO * self.weight * self.duration)

    # Новый метод базового класса.
    def __str__(self):
        return f'{self.__class__.__name__}'


def read_package(workout: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    new_training = training_types[workout](*data)
    return new_training


def main(training_workout: Training) -> None:
    """Главная функция."""
    info = training_workout.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),  # 349.252
        ('WLK', [420, 4, 20, 42]),  # 168.119
        ('WLK', [1206, 12, 6, 12]),  # 151.544
    ]

    for workout_type, workout_data in packages:
        training = read_package(workout_type, workout_data)
        main(training)
