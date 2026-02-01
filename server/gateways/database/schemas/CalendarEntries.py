class CalendarEntries(Base):
    __tablename__ = "Calendar"

    schedule_id = Column(Integer, primary_key=True, unique=True, index=True)
    scheduled_date = Column(Date, nullable=False)
    scheduled_recipe_id = Column(Integer, ForeignKey(Recipes.recipe_id), nullable=False)
    user_id = Column(Integer, ForeignKey(Users.user_id), nullable=False)