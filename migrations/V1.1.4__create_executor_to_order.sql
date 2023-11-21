BEGIN;

create table executor_to_order (

  executor_id int not null references executor(id),
  order_id int not null  references orders (id),
  primary key (executor_id, order_id),
  status VARCHAR(100) default 'sent for approval',
  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMIT;