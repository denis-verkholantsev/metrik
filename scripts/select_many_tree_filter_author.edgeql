select SkillTree { * }
filter .author.id = <uuid>$author
and .public in (select {<optional bool>$public} ?? {false, true})
order by .created desc
offset <int64>$offset
limit <int64>$limit;
