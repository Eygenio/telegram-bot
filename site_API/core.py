from settings import SiteSettings
from site_API.utils.site_api_handler import SiteApiInterface

site = SiteSettings()

headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
}

url = 'https://' + site.host_api
params = {}

site_api = SiteApiInterface()

if __name__ == "__main__":
	site_api()
