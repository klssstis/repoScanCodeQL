/**
 * @name Empty block
 * @kind problem
 * @problem.severity warning
 * @id cpp/example/empty-block
 */

import cpp

from Function fn
where 
fn.hasName("123") and
fn.hasName("321")
select fn,"hello"
