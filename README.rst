EasyIRC
~~~~~~~~

Easy IRC is an IRC toolkit to develop IRC client or bot, especially for Python/IRC beginner.

What are the Goals:

- Every core parts are replacable or expendable. They are layered considerately.
- Every behaviors are event-driven or pluggable.
- Every events are described independantly as much as possible.
- Super easy-to-write new modules.
- Batteries included - common bot features are included.
- General-purpose, still.
- Every parts are reusable. Command, event, module, entire bot or even non-easyirc based bot.

What is not a goal:

- High-performance.


Example
-------

At this time, there is no document yet.

You can follow example bot step by step:

- BasicBot_ as a starting point.
- Messages_ for general irc message hook.
- Regex_ for regex-based message hook.

.. _BasicBot: https://github.com/youknowone/easyirc/blob/master/exambot/00basic.py
.. _Context: https://github.com/youknowone/easyirc/blob/master/exambot/01context.py
.. _Messages: https://github.com/youknowone/easyirc/blob/master/exambot/10message.py
.. _Regex: https://github.com/youknowone/easyirc/blob/master/exambot/90regex.py
