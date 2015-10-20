#!/usr/bin/env python
# coding=utf-8
# 定义变量cars，space_in_a_car,drivers, passengers并赋初值
cars = 100
# 使用4.0而不用4是为了浮点数计算是保留小数
space_in_a_car = 4.0
drivers = 30
passengers = 90
#  计算cars-drivers
cars_not_driven = cars - drivers
# 赋值
cars_driven = drivers
carpool_capacity = cars_driven*space_in_a_car
average_passengers_per_car = passengers/cars_driven
# 变量car_pool_capacity没有定义
# average_passengers_per_car = car_pool_capacity /passengers
print "There are", cars, "cars available."

print "There are only",drivers, "drivers available."

print "There will be", cars_not_driven, "empty cars today."

print "We can transport", carpool_capacity, "people today."

print "We have", passengers, "to carpool today."
print "We hava to put about",average_passengers_per_car, "in each car."


