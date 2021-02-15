import inspect
import sys
import tkinter
from logging import Logger
from os import path
from typing import Union, Dict, Type, List, Callable, Any, Iterable

from .style import Style
from .widgets import PopUp


class Stage(tkinter.Frame):
	def __init__(self, style: Style, __file___: str, logger: Logger = None, non_frozen_path_join: str = '..', frozen_path_join: str = ''):
		"""
		Class for managing scenes.\n

		:param style: Style()
		:param __file___: __file__
		:param logger: Used for logging tkinter exceptions
		:param non_frozen_path_join: join to self.path() if not frozen (runned as python script)
		:param frozen_path_join: join to self.path() if frozen (runned as exe bunded by PyInstaller)
		"""
		super().__init__(tkinter.Tk(), bg=style.bg)
		if logger:
			self.master.report_callback_exception = lambda exc, val, tb: logger.exception('tkinter')
		self.style = style
		self._path = Stage.gen_path(__file___, non_frozen_path_join, frozen_path_join)
		self._active: Union['Scene', type] = type("TempScene", (), {'deactivate': lambda: None})
		self._scenes: Dict[str, 'Scene'] = {}
		self._kwargs: dict = {}
		self.__popup_active: bool = False

		self.master.bind('<Key>', self._typed)

	def path(self, *_join: str) -> str:
		"""
		Returns path to main/exe file.\n

		:param _join: Same as os.path.join()
		:return: path to main/exe file
		"""
		return path.join(self._path, *_join)

	@staticmethod
	def gen_path(__file___: str, non_frozen_path_join: str = '..', frozen_path_join: str = '') -> str:
		"""
		Used when project path is needed before Stage is created.\n
		After you have access to Stage object use path() method.\n
		Returns path to main/exe file.\n

		:param __file___: Pass __file__
		:param non_frozen_path_join: join to path if not frozen (runned as python script)
		:param frozen_path_join: join to path if frozen (runned as exe bunded by PyInstaller)
		:return: path to main/exe file
		"""
		if getattr(sys, 'frozen', False):
			tmp = path.join(path.dirname(sys.executable), frozen_path_join)
		else:
			tmp = path.join(path.dirname(__file___), non_frozen_path_join)
		return path.realpath(tmp)

	def is_active(self, scene: 'Scene') -> bool:
		return self._active is scene and not self.__popup_active

	def args(self, **kwargs) -> 'Stage':
		"""
		Specifies kwargs which will be parsed to Scenes __init__.\n
		:param kwargs: **kwargs
		:return: Stage (self)
		"""
		self._kwargs = kwargs
		return self

	def add(self, name: str, scene: Type['Scene']) -> 'Stage':
		"""
		Add scene.\n

		:param name: Name/Key of the scene. Case insensitive.
		:param scene: Class which inherits Scene (class not object)
		:return: Stage (self)
		"""
		kw = {}
		for arg in inspect.getfullargspec(scene).args[2:]:
			kw[arg] = self._kwargs.get(arg, None)
		self._scenes[name.lower()] = scene(self, **kw)
		return self

	def add_all(self, scenes: Iterable) -> 'Stage':
		"""
		Add scenes from list.\n
		Example: `Stage.add_all(globals().values())`\n

		:param scenes: List of classes which inherits Scene (class not object) (everything else in list is ignored)
		:return: Stage (self)
		"""
		for scene in scenes:
			if inspect.isclass(scene) and issubclass(scene, Scene) and scene is not Scene:
				self.add(scene.name, scene)
		return self

	def __getitem__(self, name: str) -> 'Scene':
		"""
		Get specific scene. Any other way of getting scenes is discouraged.\n

		:param name: Name/Key of Scene. Automatically converted to lower case.
		:return: Scene object
		"""
		return self._scenes.get(name.lower())

	def _typed(self, event) -> None:
		"""
		This method is not meant to be called manually.\n
		Called every time user preses key while window focused.\n
		And calls active scene typed(event) method.\n

		:param event: tkinter bind <Ket> event
		:return: None
		"""
		self._active.typed(event)

	def switch(self, to: str, whisper=None) -> None:
		"""
		Switches scenes. Any other way of switching scenes is discouraged.\n
		1. Calls active scene deactivate() method.\n
		2. Replaces active scene with new one (`to` param).\n
		3. Calls activate() on (new) active scene.\n
		(4. Focus active scene).\n

		:param to: Scene switching to. Case insensitive (if type str is given)
		:param whisper: Hand over to `to` scene as whisper
		:return: None
		"""
		s = self._scenes.get(to.lower())
		if s is None:
			raise Exception(f"No Scene named: '{to}'")
		self._active.deactivate()
		self._active = s
		self._active.activate(whisper)
		self._active.focus_set()

	def tick(self) -> None:
		"""
		This method is not meant to be called manually.\n
		Called every 10 ticks.\n

		:return: None
		"""
		self._active.tick()
		self.after(10, self.tick)

	def run(self, /, scene: Union[Type['Scene'], str], whisper=None, *, pack: bool = True, enable_tick: bool = True) -> None:
		"""
		Call this to show window and run mainloop. Any other way of running mainloop is discouraged.\n

		:param scene: Scene to show after start
		:param whisper: whisper to scene
		:param pack: Pack stage
		:param enable_tick: Do you not want to use tick() methods? Set this to False (could save some process power idk)
		:return: None
		"""
		if pack:
			self.pack(fill='both', expand=True)
		self.switch(scene, whisper)
		if enable_tick:
			self.master.after(1, self.tick)
		self.master.mainloop()

	def basic_popup(self, title: str, message: str, options: List[str]) -> str:  # TODO Make this as PopUp subclass
		root = tkinter.Toplevel()
		root.wm_minsize(200, 0)
		root.resizable(False, False)
		root.title(title)
		tkinter.Label(root, text=message, bg=self.style.bg, fg=self.style.fg).pack(fill='both')
		frame = tkinter.Frame(root, bg=self.style.bg)
		out = tkinter.StringVar()

		def on_closing():
			root.destroy()
			root.quit()

		def com(text):
			out.set(text)
			on_closing()

		root.protocol("WM_DELETE_WINDOW", on_closing)
		[tkinter.Button(frame, command=lambda x=x: com(x), text=x, bg=self.style.bg, fg=self.style.fg).pack(fill='both', side='right') for x in options]
		frame.pack(fill='both')
		root.grab_set()
		self.__popup_active = True
		root.mainloop()
		self.__popup_active = False
		root.grab_release()
		return out.get()

	def frame_popup(self, popup: Type[PopUp], title: str = '', callback: Callable[[Any], None] = None, whisper=None, style: Style = None, **kw):
		def on_closing():
			root.destroy()
			root.quit()

		root = tkinter.Toplevel()
		root.wm_minsize(200, 0)
		root.resizable(False, False)
		root.title(title)
		p = popup(root, stage=self, close=on_closing, style=style, whisper=whisper, **kw).inline_pack()
		root.protocol("WM_DELETE_WINDOW", on_closing)
		root.grab_set()
		self.__popup_active = True
		root.mainloop()
		self.__popup_active = False
		root.grab_release()
		callback(p.whisper)


class Scene(tkinter.Frame):
	name: str = ''

	def __init__(self, stage: Stage, style: Style = None):
		self.stage: Stage = stage
		self.style: Style = style if style else self.stage.style
		super().__init__(stage, bg=self.style.bg)

	def is_active(self) -> bool:
		return self.stage.is_active(self)

	def tick(self) -> None:
		"""
		Overwrite me.\n
		This method is not meant to be called manually.\n
		Called every 10 ticks.\n

		:return: None
		"""
		pass

	def typed(self, event) -> None:
		"""
		Overwrite me.\n
		This method is not meant to be called manually.\n
		Called every time user preses key while window focused.\n

		:param event: tkinter bind <Ket> event
		:return: None
		"""
		pass

	def activate(self, whisper=None) -> None:
		"""
		Overwrite me.\n
		This method is not meant to be called manually.\n
		Called every time this scene is activated/showed.\n
		This method should pack scene (self.pack()).\n

		:return: None
		"""
		self.pack(fill='both', expand=True)

	def deactivate(self) -> None:
		"""
		Overwrite me.\n
		This method is not meant to be called manually.\n
		Called when stage is switching to another scene (from this one).\n
		This method should unpack whole scene. (self.pack_forget()).\n

		:return: None
		"""
		self.pack_forget()
