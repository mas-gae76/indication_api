from rest_framework import serializers
from .models import History, Counter, User
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Sum


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Counter
        extra_kwargs = {
                            'type': {'read_only': True},
                            'user': {'read_only': True}
                       }
        fields = ['name', 'user', 'value']


# класс для получения всех переданных показаний за месяц
class HistoryDaySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, instance):
        return []

    class Meta:
        model = History
        fields = ['date', 'consumption', 'value', 'type', 'children']


# класс для получения годовых показаний
class HistoryYearSerializer(serializers.Serializer):
    period = serializers.SerializerMethodField()
    consumption = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_period(self, instance):
        return self.instance[0].date.year

    def get_consumption(self, instance):
        total_consumption = self.instance.aggregate(total=Sum('consumption'))
        return total_consumption['total']

    def get_value(self, instance):
        return self.instance.latest('value').value

    def get_type(self, instance):
        return None

    def get_children(self, instance):
        months = set(i["month"] for i in self.instance.annotate(month=ExtractMonth('date')).values('month').distinct().values())
        children = []
        for month in reversed(list(months)):
            children.append(HistoryMonthSerializer(self.instance.filter(date__month=month), many=False).data)
        return children


# класс для получения месячных показаний
class HistoryMonthSerializer(HistoryYearSerializer):
    def get_period(self, instance):
        return self.instance[0].date.strftime('%B')

    def get_children(self, instance):
        children = []
        for i in self.instance:
            children.append(HistoryDaySerializer(i, many=False).data)
        return children


# класс для получения data
class HistoryDataSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        """
        предварительная фильтрация перед получением истории показаний
        """
        all_history = self.instance.history_set.all()
        start_date = self.context['start_date']
        print(start_date)
        end_date = self.context['end_date']
        print(end_date)
        if start_date and end_date:
            all_history = all_history.filter(date__range=[start_date, end_date])
        years = set(i["year"] for i in all_history.annotate(year=ExtractYear('date')).values('year').distinct().values())
        data = []
        for year in reversed(list(years)):
            data.append(HistoryYearSerializer(all_history.filter(date__year=year), many=False).data)
        return data
