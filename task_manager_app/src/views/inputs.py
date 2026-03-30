from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from views.buttons import YellowButton
from views.category_selector import CategorySelector
from views.category_button import CategoryButton
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from models.category import Category
from controller.category_controller import CategoryController
from kivy.properties import ObjectProperty

Builder.load_file("views/Input.kv")

class InputFrame(MDBoxLayout):
    def __init__(self, main_window, controller: CategoryController, **kwargs):
        super().__init__(**kwargs)
        self.main_window = main_window
        self.controller = controller
        self.catlist = CategorySelector(self.controller)
        self.ids.extra_fields.add_widget(self.catlist)
    

    def add_category(self, category: Category):
        """add category widget to category selection group"""
        groupname = self.catlist.groupname
        btn = CategoryButton(category)
        btn.group = groupname
        self.catlist.add_widget(btn)

    def on_touch_down(self, touch):
        # This helps with the touch target for the descriptions drop down
        if self.ids.task_name.collide_point(*touch.pos):
            self.ids.task_name.focus = True
            
        return super().on_touch_down(touch)

    def expand_menu(self, has_focus: bool) -> None:
        if has_focus:
            Clock.schedule_once(self.start_animation, 0.1)

    def start_animation(self, dt) -> None:
        # The animations live here
        self.ids.extra_fields.disabled = False
        
        """anim_main = Animation(height= self.minimum_height, duration=0.2)
        anim_main.start(self)
        
        anim_fields = Animation(height= self.minimum_height, opacity=1, duration=0.2)
        anim_fields.start(self.ids.extra_fields)"""

        self.ids.extra_fields.disabled = False
        Animation(height=self.ids.extra_fields.minimum_height, opacity=1, duration=0.2).start(self.ids.extra_fields)
    
    
    def add_task(self) -> None:
        name = self.ids.task_name.text
        desc = self.ids.description.text
        deadline = self.ids.deadline.text
        category = self.ids.cat_list.get_selected_category()

        self.main_window.add_todo_item(name, desc, deadline, category)
        self.ids.extra_fields.disabled = True

        anim_main = Animation(height=dp(50), duration=0.2)
        anim_main.start(self)
        
        anim_fields = Animation(height=dp(0), opacity=0, duration=0.2)
        anim_fields.start(self.ids.extra_fields)