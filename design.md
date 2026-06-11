# Project summary

A lightweight study planner web application written in Python with the Django framework.

The project is intended to improve my understanding of Django and wider web application development, particularly back-end design.

# Core Loop

- User creates items.
- Items appear collated to user on board.
- User uses global view to efficiently study.

# Project Pillars

- Django web framework.
- Server-side rendering.
- Fast data manipulation with lightweight but intuitive UI.
- Clean and understandable architecture.
- Fully completable and polish-able.

# Minimum Viable Product

- Website in browser.
- User registration and login.
- Items.
- Tags.
- Calendar.
- Agenda.
- Repeating items.
- Item collation on boards by tags.

# Stretch Features

- Sub-items.
- Settings.
- Positive visual feedback on progression.
- Personal study planner (using algorithm).
- Pull deadlines from Moodle.
- Native mobile (and maybe desktop) application with Flutter.

# Kanban

## Todo

- Calendar.
  - HTMX item window on RHS (span page on mobile).
  - HTMX tag window on RHS (left of item window)(span page on mobile).
- Agenda.
- Repeating items.
- Item collation by tags in calendar and agenda boards.

- Quality of life:
  - Start datetime now button
  - End datetime autofills to start datetime
  - +0, +0.25, +0.5, +1 hour, +1 day buttons for end datetime (javascript)
- simple user feedback form

## In-progress

- Calendar.
  - Improve efficiency (through AI peer review) of board.calendar.
  - Add previous months to htmx scrolling.
    - stop it from scrolling up infinitely really fast

## Done

- Website in browser.
- User registration and login.
- Items.
- Tags.
