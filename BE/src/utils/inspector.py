from user_agents import parse

class UserInspector:
    @staticmethod
    def get_client_ip(request):
        x_forwarded = request.headers.get("X-Forwarded-For")
        return x_forwarded.split(",")[0].strip() if x_forwarded else request.remote_addr

    @staticmethod
    def get_user_agent_info(request):
        ua_string = request.headers.get("User-Agent", "")
        ua = parse(ua_string)
        return {
            "browser": f"{ua.browser.family} {ua.browser.version_string}",
            "os": f"{ua.os.family} {ua.os.version_string}",
            "device": ua.device.family if ua.device.family != "Other" else "PC/Laptop"
        }