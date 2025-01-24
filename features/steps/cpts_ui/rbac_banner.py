# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.rbac_banner import RBACBannerPage


############################################################################
# THEN STEPS
############################################################################


@then("I can see the RBAC banner")
def i_can_see_the_rbac_banner(context):
    rbac_banner = RBACBannerPage(context.page)

    expect(rbac_banner.rbac_banner).to_be_visible()
    expect(rbac_banner.rbac_content).to_be_visible()

    assert rbac_banner.rbac_content.text_content(), "No banner content"
    assert rbac_banner.banner_text.match(
        str(rbac_banner.rbac_content.text_content())
    ), "Banner content does not match expected pattern"


@then("I can not see the RBAC banner")
def i_can_not_see_the_rbac_banner(context):
    rbac_banner = RBACBannerPage(context.page)

    expect(rbac_banner.rbac_banner).not_to_be_visible()
    expect(rbac_banner.rbac_content).not_to_be_visible()
