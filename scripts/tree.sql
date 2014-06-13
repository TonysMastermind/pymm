drop table tree_node;
create table tree_node (
       tree_id text PRIMARY KEY,
       parent_id text,
       root int,
       score int,
       distance_from_root int,
       problem_size int,
       max_subproblem_size int,
       child_count,
       root_in_problem int,
       optimal int,
       total_moves int,
       max_depth int
);
