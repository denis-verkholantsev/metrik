with
    user := (select User filter .id = <uuid>$user_uid)
    update SkillTree
    filter .id = <uuid>$tree_uid
    and .author = user
    set {
        likes -= user
    }
;
