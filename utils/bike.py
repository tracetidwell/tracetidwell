import numpy as np
import pandas as pd
import math
from .gpxparser import GPXParser

class Bike:
	
	g = 9.81

	def __init__(self, bike_gpx, bike_ftp, mass, intensities, grades, 
				 crr=0.002475, rho=1.29, cda=0.3215, rpm=90):
		self.bike_gpx = bike_gpx
		self.bike_ftp = bike_ftp
		self.mass = mass
		self.intensities = intensities
		self.grades = grades
		self.crr = crr
		self.rho = rho
		self.cda = cda
		self.rpm = 90
		self.crank = rpm * 2 * math.pi / 60 * 0.165
		
	def predict(self):

		def course_data(self):
			gpx = GPXParser(self.bike_gpx)
			lat = gpx.lat_values()
			lon = gpx.lon_values()
			ele = gpx.ele_values()
			data = np.append(lat.T, lon.T, axis=1)
			data = np.append(data, ele.T, axis=1)
			columns = ['lat', 'lon', 'ele']
			df = pd.DataFrame(data, columns = columns)
			#sometimes the file starts recording while in place
			#we remove duplicates
			df.drop_duplicates(inplace=True)
	
			#we then reset the index to start at 0 and run until the end
			df.reset_index(drop=True, inplace=True)
			#unique, indices = np.unique(data, return_index=True)
	
			self.lat = df.values[:, 0]
			self.lon = df.values[:, 1]
			self.ele = df.values[:, 2]
	
		def calc_distance(self):
			sum_phi = (self.lat[1:] + self.lat[:-1]) * math.pi / 180
			del_lam = (self.lon[1:] - self.lon[:-1]) * math.pi / 180
			x = del_lam * np.cos(sum_phi/2)
			y = (self.lat[1:] - self.lat[:-1]) * math.pi / 180
			self.distance = 6371000 * np.sqrt(np.power(x, 2) + np.power(y, 2))
			self.total_distance = (sum(self.distance) / 1000)# * 0.621371
	
		def calc_grade(self):
			self.grade = np.array(self.ele[1:] - self.ele[:-1]) / self.distance
	
		def calc_theta(self):
			self.theta = np.arctan(self.grade)
	
		def calc_power(self):
			power = np.zeros(len(self.grade)) + self.bike_ftp * self.intensities[0]
			for i in range(len(self.grades)):
				power[self.grade >= self.grades[i]] = self.bike_ftp * self.intensities[i+1]
			self.power = power
	
		def calc_velocity(self):
			a = np.zeros((len(self.power), 1)) + (self.rho * self.cda) / 2
			b = np.zeros((len(self.power), 1))
			c = self.mass * 9.81 * (self.crr * np.cos(self.theta) + np.sin(self.theta))
			c = c.reshape(c.shape[0], 1)
			d = -self.power.reshape(self.power.shape[0], 1)

			coeffs = np.append(a, b, axis=1)
			coeffs = np.append(coeffs, c, axis=1)
			coeffs = np.append(coeffs, d, axis=1)
			self.coeffs = coeffs

			velocity = np.zeros(len(coeffs))
			for i in range(coeffs.shape[0]):
				try:
					roots = np.roots([coeffs[i, 0], coeffs[i, 1], coeffs[i, 2], coeffs[i, 3]])
					velocity[i] = np.real(roots[np.imag(roots) == 0])[0]
				except:
					print(i)

			self.velocity = velocity
	
			# a = 0.5 * self.rho * self.cda
			# c = (self.mass * 9.81 ) * (np.sin(self.theta) + self.crr * np.cos(self.theta))
			# d = -self.power
			# v = []
			# for i,_ in enumerate(c):
			#     v.append(np.max(np.real(np.roots([a, 0, c[i], d[i]]))))
			# self.velocity = np.array(v)
	
		def calc_time(self):
			self.time = self.distance / self.velocity
			self.total_time = sum(self.time)/3600
	
		def avg_velocity(self):
			self.avg_velocity = (self.total_distance / self.total_time)
			
		def avg_power(self):
			self.avg_power = sum(self.power * self.distance) / sum(self.distance)
			
		def norm_power(self):
			norm = np.zeros(len(self.power)-30)
			for i, _ in enumerate(norm):
				norm[i] = sum(self.power[i:i+30]) / 30
			self.norm_power = int(round(np.power(sum(np.power(norm, 4)) / len(norm), 0.25)))
			
		def intensity_factor(self):
			self.intensity_factor = self.norm_power / self.bike_ftp
			
		def tss(self):
			self.tss = self.intensity_factor **2 * self.total_time * 100
			
		def vi(self):
			self.vi = self.norm_power / self.avg_power
			
		course_data(self)
		calc_distance(self)
		calc_grade(self)
		calc_theta(self)
		calc_power(self)
		calc_velocity(self)
		calc_time(self)
		avg_velocity(self)
		avg_power(self)
		norm_power(self)
		intensity_factor(self)
		tss(self)
		vi(self)
