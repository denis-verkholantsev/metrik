select User{
    *,
    external_links := .<user[is ExternalLink] { url }
}
filter .id=<uuid>$uid;
