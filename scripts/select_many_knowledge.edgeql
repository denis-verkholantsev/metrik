select Knowledge {*, author, skill}
filter .skill.id=<uuid>$skill_uid
   and .author.id=<uuid>$user_uid
;
