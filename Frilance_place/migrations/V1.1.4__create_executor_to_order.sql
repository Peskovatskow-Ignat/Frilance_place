BEGIN;

create table executor_to_order (

  executor_id int not null references executor(id),
  order_id int not null  references orders(id),
  primary key (executor_id, order_id)
);

COMMIT;