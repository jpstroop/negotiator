from negotiator import AcceptParameters
from negotiator import ContentNegotiator
from negotiator import ContentType
from negotiator import Language


class ContentTypeTests:
    def test_text_plain_only(self):
        """
        text/plain only
        """
        client_accept = "text/plain"
        server = [AcceptParameters(ContentType("text/plain"))]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "text/plain"

    def test_without_q_values(self):
        """
        application/atom+xml vs application/rdf+xml without q values
        """
        client_accept = "application/atom+xml, application/rdf+xml"
        server = [
            AcceptParameters(ContentType("application/rdf+xml")),
            AcceptParameters(ContentType("application/atom+xml")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "application/atom+xml"

    def test_with_q_values(self):
        """
        application/atom+xml vs application/rdf+xml with q values
        """
        client_accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9"
        server = [
            AcceptParameters(ContentType("application/rdf+xml")),
            AcceptParameters(ContentType("application/atom+xml")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "application/rdf+xml"

    def test_with_mixed_q_values(self):
        """
        application/atom+xml vs application/rdf+xml vs text/html with mixed q values
        """
        client_accept = (
            "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
        )
        server = [
            AcceptParameters(ContentType("application/rdf+xml")),
            AcceptParameters(ContentType("application/atom+xml")),
            AcceptParameters(ContentType("text/html")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "text/html"

    def test_unsupported_by_server(self):
        """
        text/plain only, unsupported by server
        """
        client_accept = "text/plain"
        server = [AcceptParameters(ContentType("text/html"))]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert accept_parameters is None

    def test_most_preferred_unavailable(self):
        """
        application/atom+xml vs application/rdf+xml vs text/html with mixed q
        values, most preferred unavailable
        """
        client_accept = (
            "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
        )
        server = [
            AcceptParameters(ContentType("application/rdf+xml")),
            AcceptParameters(ContentType("application/atom+xml")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "application/rdf+xml"

    def test_mixed_q_values_most_preferred_available(self):
        """
        application/atom+xml vs application/rdf+xml vs text/html with mixed q
        values, most preferred available
        """
        client_accept = (
            "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
        )
        server = [
            AcceptParameters(ContentType("application/rdf+xml")),
            AcceptParameters(ContentType("text/html")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "text/html"

    def test_atom_with_type_feed_supported_by_server(self):
        """
        application/atom+xml;type=feed supported by server
        """
        client_accept = "application/atom+xml;type=feed"
        server = [
            AcceptParameters(ContentType("application/atom+xml;type=feed"))
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert (
            str(accept_parameters.content_type)
            == "application/atom+xml;type=feed"
        )

    def test_image_wildcard_supported_by_server(self):
        """
        image/* supported by server
        """
        client_accept = "image/*"
        server = [
            AcceptParameters(ContentType("text/plain")),
            AcceptParameters(ContentType("image/png")),
            AcceptParameters(ContentType("image/jpeg")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "image/png"

    def test_any_supported_by_server(self):
        """
        */* supported by server
        """
        client_accept = "*/*"
        server = [
            AcceptParameters(ContentType("text/plain")),
            AcceptParameters(ContentType("image/png")),
            AcceptParameters(ContentType("image/jpeg")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept=client_accept)
        assert str(accept_parameters.content_type) == "text/plain"


class LanguageTests:
    def test_en_only(self):
        """
        en only
        """
        accept_language = "en"
        server = [AcceptParameters(language=Language("en"))]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "en"

    def test_without_q_values(self):
        """
        en vs de without q values
        """
        accept_language = "en, de"
        server = [
            AcceptParameters(language=Language("en")),
            AcceptParameters(language=Language("de")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "en"

    def test_with_q_values(self):
        """
        fr vs no with q values
        """
        accept_language = "fr;q=0.7, no;q=0.8"
        server = [
            AcceptParameters(language=Language("fr")),
            AcceptParameters(language=Language("no")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "no"

    def test_with_mixed_q_values(self):
        """
        en vs de vs fr with mixed q values
        """
        accept_language = "en;q=0.6, de;q=0.9, fr"
        server = [
            AcceptParameters(language=Language("en")),
            AcceptParameters(language=Language("de")),
            AcceptParameters(language=Language("fr")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "fr"

    def test_unsupported_by_server(self):
        """
        en only, unsupported by server
        """
        accept_language = "en"
        server = [AcceptParameters(language=Language("de"))]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert accept_parameters is None

    def test_mixed_q_most_preferred_unavailable(self):
        """
        en vs no vs de with mixed q values, most preferred unavailable
        """
        accept_language = "en;q=0.6, no;q=0.9, de"
        server = [
            AcceptParameters(language=Language("en")),
            AcceptParameters(language=Language("no")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "no"

    def test_mixed_q_values_most_preferred_available(self):
        """
        en vs no vs de with mixed q values, most preferred available
        """
        accept_language = "en;q=0.6, no;q=0.9, de"
        server = [
            AcceptParameters(language=Language("no")),
            AcceptParameters(language=Language("de")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "de"

    def test_supported_by_server(self):
        """
        en-gb supported by server
        """
        accept_language = "en-gb"
        server = [AcceptParameters(language=Language("en-gb"))]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "en-gb"

    def test_unsupported_by_server(self):
        """
        en-gb, unsupported by server
        """
        accept_language = "en-gb"
        server = [AcceptParameters(language=Language("en"))]
        cn = ContentNegotiator(
            acceptable=server, ignore_language_variants=False
        )
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert accept_parameters is None

    def test_supported_by_server_through_language_variants(self):
        """
        en-gb, supported by server through language variants
        """
        accept_language = "en-gb"
        server = [AcceptParameters(language=Language("en"))]
        cn = ContentNegotiator(
            acceptable=server, ignore_language_variants=True
        )
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "en"

    def test_partially_supported_by_server(self):
        """
        en, partially supported by server
        """
        accept_language = "en"
        server = [AcceptParameters(language=Language("en-gb"))]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "en-gb"

    def test_wildcard_by_itself(self):
        """
        * by itself
        """
        accept_language = "*"
        server = [
            AcceptParameters(language=Language("no")),
            AcceptParameters(language=Language("de")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "no"

    def test_image_wildcard_supported_by_serverwith_other_options_primary_option_unsupported(self):
        """
        * with other options, primary option unsupported
        """
        accept_language = "en, *"
        server = [
            AcceptParameters(language=Language("no")),
            AcceptParameters(language=Language("de")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "no"

    def test_image_wildcard_supported_by_serverwith_other_options_primary_option_supported(self):
        """
        * with other options, primary option supported
        """
        accept_language = "en, *"
        server = [
            AcceptParameters(language=Language("en")),
            AcceptParameters(language=Language("de")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(accept_language=accept_language)
        assert str(accept_parameters.language) == "en"


class ContentTypeAndLanguageTests:
    def test_content_type_and_language_specified(self):
        """
        content type and language specified
        """
        accept = "text/html"
        accept_lang = "en"
        server = [AcceptParameters(ContentType("text/html"), Language("en"))]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(
            accept=accept, accept_language=accept_lang
        )
        assert str(accept_parameters.content_type) == "text/html"
        assert str(accept_parameters.language) == "en"

    def test_two_content_types_and_one_language_specified(self):
        """
        Two content types and one language specified
        """
        accept = "text/html, text/plain"
        accept_lang = "en"
        server = [
            AcceptParameters(ContentType("text/html"), Language("de")),
            AcceptParameters(ContentType("text/plain"), Language("en")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(
            accept=accept, accept_language=accept_lang
        )
        assert str(accept_parameters.content_type) == "text/plain"
        assert str(accept_parameters.language) == "en"

    def test_two_content_types_and_two_languages_specified(self):
        """
        Two content types and 2 languages specified
        """
        accept = "text/html, text/plain"
        accept_lang = "en, de"
        server = [
            AcceptParameters(ContentType("text/html"), Language("de")),
            AcceptParameters(ContentType("text/plain"), Language("en")),
        ]
        cn = ContentNegotiator(acceptable=server)
        accept_parameters = cn.negotiate(
            accept=accept, accept_language=accept_lang
        )
        assert str(accept_parameters.content_type) == "text/html"
        assert str(accept_parameters.language) == "de"

    def test_two_content_types_and_one_language_specified_with_weights(self):
        """
        Two content types and one language specified, with weights
        """
        weights = {
            "content_type": 2.0,
            "language": 1.0,
            "charset": 1.0,
            "encoding": 1.0,
        }
        accept = "text/html, text/plain"
        accept_lang = "en"
        server = [
            AcceptParameters(ContentType("text/html"), Language("de")),
            AcceptParameters(ContentType("text/plain"), Language("en")),
        ]
        cn = ContentNegotiator(acceptable=server, weights=weights)
        accept_parameters = cn.negotiate(
            accept=accept, accept_language=accept_lang
        )
        assert str(accept_parameters.content_type) == "text/plain"
        assert str(accept_parameters.language) == "en"
