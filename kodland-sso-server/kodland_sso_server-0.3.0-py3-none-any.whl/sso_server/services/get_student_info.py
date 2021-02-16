from django.core.exceptions import ObjectDoesNotExist

from basics.models import User, Student


class GetStudentInfo(object):
	"""
	получение данных о пользователе (студенте/преподавателе)
	"""
	def __init__(self, user_id: int):
		try:
			self.user = User.objects.get(pk=user_id)
		except ObjectDoesNotExist:
			self.user = None
			
	def get_student_info_by_param(self, param_name: str) -> dict:
		result = {
			'value': None
		}
		
		if self.user:
			try:
				student = Student.objects.get(user=self.user)
			except ObjectDoesNotExist:
				pass
			else:
				try:
					value = getattr(student, param_name)()
					result.update({'value': value})
				except AttributeError:
					pass
				except TypeError:
					value = getattr(student, param_name)
					result.update({'value': str(value)})
		
		return result
