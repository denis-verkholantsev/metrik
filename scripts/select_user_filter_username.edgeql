select User{
    *,
    external_links := .<user[is ExternalLink] { url }
}
filter .username=<str>$username;
