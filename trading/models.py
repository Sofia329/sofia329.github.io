from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class TickerMeta(models.Model):
    ticker = models.CharField(max_length=20, unique=True)
    short_name = models.CharField(max_length=255, null=True)
    long_name = models.CharField(max_length=255, null=True)
    quote_type = models.CharField(max_length=50, null=True)
    currency = models.CharField(max_length=10, null=True)
    exchange = models.CharField(max_length=50, null=True)
    time = models.DateTimeField(auto_now = True)

    def serialize(self):
        return {
            "ticker": self.ticker,
            "short_name": self.short_name,
            "long_name": self.long_name,
            "quote_type": self.quote_type,
            "currency": self.currency,
            "exchange": self.exchange,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
        }


class Valuation(models.Model):
    ticker = models.OneToOneField(TickerMeta, on_delete = models.CASCADE, related_name = "valuation" )
    market_cap = models.FloatField(null=True)
    trailing_pe = models.FloatField (null=True)
    forward_pe = models.FloatField (null=True)
    price_to_book = models.DecimalField (max_digits = 10, decimal_places = 4, null=True)
    enterprise_value = models.BigIntegerField (null=True)


    def serialize(self):
        return {
            "market_cap": self.market_cap,
            "trailing_pe": self.trailing_pe,
            "forward_pe": self.forward_pe,
            "price_to_book": self.price_to_book,
            "enterprise_value": self.enterprise_value,
        }

class Dividend(models.Model):
    ticker = models.OneToOneField( TickerMeta,  on_delete = models.CASCADE, related_name = "dividend" )
    dividend_rate = models.FloatField(null=True)
    dividend_yield = models.FloatField(null=True)
    ex_dividend_date = models.DateTimeField(null=True)
    dividend_date = models.DateTimeField(null=True)
    payout_ratio = models.DecimalField (max_digits = 10, decimal_places = 2, null=True)

    def serialize(self):
        return {
            "dividend_rate": self.dividend_rate,
            "dividend_yield": self.dividend_yield,
            "ex_dividend_date": self.ex_dividend_date.strftime("%b %d %Y, %I:%M %p") if self.ex_dividend_date else None,
            "dividend_date": self.dividend_date.strftime("%b %d %Y, %I:%M %p") if self.dividend_date else None,
            "payout_ratio": self.payout_ratio,
        }


class Risk(models.Model):
    ticker = models.OneToOneField( TickerMeta,  on_delete = models.CASCADE, related_name = "risk" )
    beta = models.FloatField(null=True)
    short_ratio = models.FloatField(null=True)

    def serialize(self):
        return {
            "beta": self.beta,
            "short_ratio": self.short_ratio,
        }

class Earning(models.Model):
    ticker = models.OneToOneField(TickerMeta, on_delete=models.CASCADE, related_name="earning")
    earning_timestamp = models.DateTimeField(null=True)
    earning_quarterly_growth = models.FloatField(null=True)
    earning_growth = models.FloatField(null=True)
    revenue_growth = models.FloatField(null=True)
    trailing_eps = models.FloatField(null=True)
    forward_eps = models.FloatField(null=True)

    def serialize(self):
        return {
            "earning_timestamp": self.earning_timestamp,
            "earning_quarterly_growth": self.earning_quarterly_growth,
            "earning_growth": self.earning_growth,
            "revenue_growth": self.revenue_growth,
            "trailing_eps": self.trailing_eps,
            "forward_eps": self.forward_eps,
        }

class AnalystRating(models.Model):
    ticker = models.OneToOneField(TickerMeta, on_delete=models.CASCADE, related_name="analyst_rating")
    target_high_price = models.FloatField(null=True)
    target_low_price = models.FloatField(null=True)
    recommendation_mean = models.FloatField(null=True)
    average_analyst_rating = models.CharField(max_length=20, null=True)

    def serialize(self):
        return {
            "target_high_price": self.target_high_price,
            "target_low_price": self.target_low_price,
            "recommendation_mean": self.recommendation_mean,
            "average_analyst_rating": self.average_analyst_rating,
        }
