select User{
    *,
    external_links := .<user[is ExternalLink] { url }
}
filter .email=<str>$email;
