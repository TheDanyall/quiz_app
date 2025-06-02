from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(
            text="English Quiz", 
            font_size=dp(28),
            halign='center',
            color=get_color_from_hex('#FFFFFF'),
            font_name='Arial',
            size_hint=(1, 0.3)
        )
        
        instructions = Label(
            text="This quiz contains 6 multiple-choice questions.\nYou have 10 seconds for each question.", 
            font_size=dp(18),
            halign='center',
            color=get_color_from_hex('#FFFF00'),
            font_name='Arial',
            size_hint=(1, 0.3))
        
        start_btn = Button(
            text="Start Quiz", 
            size_hint=(1, 0.2),
            font_size=dp(22),
            background_color=get_color_from_hex('#0066CC'),
            color=get_color_from_hex('#FFFFFF'),
            font_name='Arial'
        )
        start_btn.bind(on_press=self.start_survey)
        
        layout.add_widget(title)
        layout.add_widget(instructions)
        layout.add_widget(start_btn)
        
        self.add_widget(layout)

    def start_survey(self, instance):
        self.manager.current = 'question_1'


class QuestionScreen(Screen):
    def __init__(self, question, options, correct_answer, question_num, total_questions, next_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question
        self.correct_answer = correct_answer
        self.next_screen = next_screen
        self.time_left = 10  
        self.answered = False
        self.user_answer = None
        self.timer_event = None

        
        self.timer_label = Label(
            text=f"Time left: {self.time_left} seconds",
            font_size=dp(16),
            halign='right',
            color=get_color_from_hex('#FF5555'),
            font_name='Arial'
        )

        
        self.question_num_label = Label(
            text=f"Question {question_num} of {total_questions}",
            font_size=dp(16),
            halign='left',
            color=get_color_from_hex('#FFFFFF'),
            font_name='Arial'
        )

        
        self.question_label = Label(
            text=question,
            font_size=dp(22),
            halign='center',
            valign='top',
            color=get_color_from_hex('#FFFFFF'),
            font_name='Arial',
            bold=True,
            size_hint_y=None,
            text_size=(Window.width - dp(20), None))
        self.question_label.bind(texture_size=self.question_label.setter('size'))

       
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        header_layout.add_widget(self.question_num_label)
        header_layout.add_widget(self.timer_label)
        main_layout.add_widget(header_layout)

        
        scroll_view = ScrollView(size_hint=(1, 0.4))
        scroll_view.add_widget(self.question_label)
        main_layout.add_widget(scroll_view)

       
        options_scroll = ScrollView(size_hint=(1, 0.5))
        options_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        options_layout.bind(minimum_height=options_layout.setter('height'))

        
        self.option_buttons = []
        for i, option in enumerate(options):
            btn = Button(
                text=option,
                font_size=dp(18),
                size_hint=(1, None),
                height=dp(60),
                background_color=get_color_from_hex('#333333'),
                color=get_color_from_hex('#FFFFFF'),
                font_name='Arial',
                halign='left',
                padding=(dp(10), dp(5)),
                markup=True
            )
            btn.bind(on_press=lambda x, idx=i: self.answer_question(idx))
            options_layout.add_widget(btn)
            self.option_buttons.append(btn)

        options_scroll.add_widget(options_layout)
        main_layout.add_widget(options_scroll)

        self.add_widget(main_layout)

    def on_pre_enter(self, *args):
       
        if not self.timer_event:
            self.time_left = 10  
            self.timer_label.text = f"Time left: {self.time_left} seconds"
            self.timer_label.color = get_color_from_hex('#FF5555')
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def on_leave(self, *args):
        
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Time left: {self.time_left} seconds"
        
      
        if self.time_left <= 5:
            self.timer_label.color = get_color_from_hex('#FF0000')
        
       
        if self.time_left <= 0 and not self.answered:
            self.answer_question(None)

    def answer_question(self, answer_idx):
        if self.answered:
            return
            
        self.answered = True
        self.user_answer = answer_idx
        
        
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        
        
        self.option_buttons[self.correct_answer].background_color = get_color_from_hex('#00AA00')
        
       
        if answer_idx is not None and answer_idx != self.correct_answer:
            self.option_buttons[answer_idx].background_color = get_color_from_hex('#FF0000')
        
       
        if self.next_screen:
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', self.next_screen), 2.0)


class ResultScreen(Screen):
    def __init__(self, answers, questions, **kwargs):
        super().__init__(**kwargs)
        self.answers = answers
        self.questions = questions
        
        main_layout = BoxLayout(orientation='vertical')
        
        scroll_view = ScrollView()
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=dp(10))
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
       
        title = Label(
            text="Quiz Results", 
            font_size=dp(28),
            halign='center',
            color=get_color_from_hex('#FFFFFF'),
            font_name='Arial',
            size_hint_y=None,
            height=dp(60))
        content_layout.add_widget(title)
        
        correct_count = sum(1 for ans in answers if ans['user_answer'] == ans['correct_answer'])
        score_label = Label(
            text=f"Your score: {correct_count}/{len(questions)}",
            font_size=dp(24),
            halign='center',
            color=get_color_from_hex('#FFFF00'),
            font_name='Arial',
            size_hint_y=None,
            height=dp(50))
        content_layout.add_widget(score_label)
        
        
        for i, (ans, q) in enumerate(zip(answers, questions)):
            question_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
            
            
            question_text = Label(
                text=f"[b]Q{i+1}:[/b] {q['question']}",
                font_size=dp(18),
                halign='left',
                color=get_color_from_hex('#FFFFFF'),
                font_name='Arial',
                size_hint_y=None,
                height=dp(60),
                text_size=(Window.width - dp(20), None),
                markup=True
            )
            question_box.add_widget(question_text)
            
            
            correct_text = Label(
                text=f"Correct: {q['options'][ans['correct_answer']]}",
                font_size=dp(16),
                halign='left',
                color=get_color_from_hex('#00FF00'),
                font_name='Arial',
                size_hint_y=None,
                height=dp(30)
            )
            question_box.add_widget(correct_text)
            
           
            if ans['user_answer'] is not None:
                user_ans_text = Label(
                    text=f"Your answer: {q['options'][ans['user_answer']]}",
                    font_size=dp(16),
                    halign='left',
                    color=get_color_from_hex('#FF0000') if ans['user_answer'] != ans['correct_answer'] else get_color_from_hex('#00FF00'),
                    font_name='Arial',
                    size_hint_y=None,
                    height=dp(30)
                )
                question_box.add_widget(user_ans_text)
            else:
                no_answer_text = Label(
                    text="You didn't answer this question",
                    font_size=dp(16),
                    halign='left',
                    color=get_color_from_hex('#FF5555'),
                    font_name='Arial',
                    size_hint_y=None,
                    height=dp(30)
                )
                question_box.add_widget(no_answer_text)
            
            content_layout.add_widget(question_box)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)


class QuizApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_answers = []
    
    def build(self):
        Window.clearcolor = get_color_from_hex('#001a33')
        self.sm = ScreenManager()
        
        self.questions = [
            {
                'question': 'Which of these is NOT a meaning of Python?',
                'options': ['A snake', 'Programming language', 'A type of shoe', 'None of these'],
                'correct_answer': 2  # A type of shoe
            },
            {
                'question': 'What is Kivy used for?',
                'options': ['Mobile apps', 'Desktop apps', 'Cross-platform apps', 'All of these'],
                'correct_answer': 3  # All of these
            },
            {
                'question': 'How much time do you have for each question?',
                'options': ['60 seconds', '15 seconds', '10 seconds', '30 seconds'],
                'correct_answer': 2  # 10 seconds
            },
            {
                'question': 'Which statement about Kivy is NOT true?',
                'options': ['Uses OpenGL', 'Works only on Android', "Doesn't use SDK", 'Works with Python'],
                'correct_answer': 1  # Works only on Android
            },
            {
                'question': 'What does "cross-platform" programming mean?',
                'options': ['User can work on multiple systems', 'App runs on multiple OS', 'App has multiple languages', 'App can do multiple tasks'],
                'correct_answer': 1  # App runs on multiple OS
            },
            {
                'question': 'Which is NOT an advantage of Kivy?',
                'options': ['It is free', 'No need to compile', 'Very fast execution', 'Supports multiple OS'],
                'correct_answer': 2  # Very fast execution
            }
        ]
        
        self.sm.add_widget(StartScreen(name='start'))
        
        for i, q in enumerate(self.questions):
            next_screen = f'question_{i+2}' if i < len(self.questions)-1 else 'results'
            screen = QuestionScreen(
                question=q['question'],
                options=q['options'],
                correct_answer=q['correct_answer'],
                question_num=i+1,
                total_questions=len(self.questions),
                next_screen=next_screen,
                name=f'question_{i+1}'
            )
            screen.bind(on_pre_enter=self.save_answer)
            self.sm.add_widget(screen)
        
        return self.sm
    
    def save_answer(self, instance):
        if hasattr(instance, 'user_answer'):
            if len(self.user_answers) <= int(instance.name.split('_')[1]) - 1:
                self.user_answers.append({
                    'user_answer': instance.user_answer,
                    'correct_answer': instance.correct_answer
                })
                
                if len(self.user_answers) == len(self.questions):
                    result_screen = ResultScreen(
                        answers=self.user_answers,
                        questions=self.questions,
                        name='results'
                    )
                    self.sm.add_widget(result_screen)
                    self.sm.current = 'results'


if __name__ == '__main__':
    QuizApp().run()