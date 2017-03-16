# itsuiku


### Intro
itsuiku is the app that people can easily manage attendance for party, meeting,,,any kind of events.





### events app

- models.py

Event
- user: ForeignKey(User)
- title: CharField
- description: TextField
- schedule: ManyToManyField(Schedule)
- created: DateTimeField
- update: DateTimeField
