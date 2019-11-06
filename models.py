import os
import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE_URL'))
os.getenv('i')


class Base(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Base, self).save(*args, **kwargs)

    class Meta:
        database = db
        legacy_table_names = False


class Store(Base):
    name = pw.CharField(unique=True)


class Warehouse(Base):
    store = pw.ForeignKeyField(Store, backref='warehouses', unique=True)
    location = pw.TextField()


class Product(Base):
    name = pw.CharField(index=True)
    description = pw.TextField()
    warehouse = pw.ForeignKeyField(Warehouse, backref='products')
    color = pw.CharField(null=True)


if __name__ == "__main__":
    db.init('inv_mgmt') #initialised db!
    db.connect()
    db.create_tables([Store, Warehouse, Product])

