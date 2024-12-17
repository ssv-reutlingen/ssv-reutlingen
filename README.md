## SSV Reutlingen

ERP system for SSV Reutlingen football club

## Doctypes
To find out more about the doctypes this app includes go to your doctype list after successful install and filter for custom app "SSV Reutlingen"

## Installation
Go to your folder /frappe-bench/apps/ and run the following line with sudo permissions to download. Where branch is the branch of this repo you want to install (e.g. develop or version-13).

`bench get-app https://github.com/ssv-reutlingen/ssv-reutlingen.git --branch branch`

now where the app is downloaded we can install it with the following command where your-site.ltd is the name of your site in the /frappe-bench/sites folder

`bench --site your-site.tld install-app ssv_reutlingen`

Once done run

`bench migrate`

and

`bench clear-cache`

and you are ready to go.

#### License

MIT# ssv-reutlingen
