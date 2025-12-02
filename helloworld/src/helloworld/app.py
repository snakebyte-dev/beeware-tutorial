"""
My first application
"""
# iOS application can only be compiled on macOS :(
import faker # library to generate fake data for testing
import httpx
import toga # widget toolkit
from toga.style.pack import COLUMN, ROW # style related utility constants

def greeting(name):
   if name:
       return f"Hello, {name}"
   else:
       return "Hello, stranger"


class HelloWorld(toga.App):
    async def say_hello(self, widget):
        fake = faker.Faker()
        async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts/42")

        payload = response.json()

        await self.main_window.dialog(
            toga.InfoDialog(
                greeting(self.name_input.value),
                f"A message from {fake.name()}: {payload['body']}",
            )
        )

    def startup(self):
        main_box = toga.Box(direction=COLUMN) # it is a box that will consume all the available width, and will expand its height as content is added, but it will try to be as short as possible

        name_label = toga.Label(
            "Your name: ",
            margin=(0, 5),
        ) # Top and bottom margin 0, left and right margin 5
        self.name_input = toga.TextInput(flex=1)

        name_box = toga.Box(direction=ROW, margin=5) # content will be added horizontally, and it will try to make its width as narrow as possible. The box also has some margin - 5px on all sides.
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Say Hello!",
            on_press=self.say_hello, # handler/callback: method that is called when button is pressed
            margin=5,
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return HelloWorld()
