import src.base32 as base32
import src.base36 as base36
import src.base45 as base45
import src.base58 as base58
import src.base62 as base62
import base64
import src.base91 as base91
import src.base92 as base92
import src.base100 as base100
import src.rot13 as rot13
import src.hex as hexCode
import src.morse as morse
import src.cvecode as cvecode
import src.xxencode as xxencode
import src.buddha as buddha

from termcolor import colored

class DecodeBase:
    def __init__(self, encoded_crypto, api_call=False, image_mode=False):
        self.encoded_crypto = encoded_crypto
        self.b32_once = False
        self.b64_once = False
        self.b64_url = False
        self.encoding_ciphers = []
        self.decoded_strings = []

        # state conditions
        self.api_call = api_call
        self.image_mode_call = image_mode

    def decode(self):
        self.decode_crypto()
        return (
            self.encoding_ciphers,
            self.decoded_strings
        )

    def contains_replacement_char(self, res):
        """
        `contains_replacement_char()` checks whether the decoded base
        contains an unknown unicode, ie: invalid character.
        these are replaced with 'replacement character',
        which is '�' and 'U+FFFD' in unicode and
        also checks for unicode chars after `127`.
        """
        if u'\ufffd' in res: return True
        else:
            count = 0
            for char in res:
                if ord(char) > 127: count += 1
            return True if count > 0 else False

    def process_decode(self, decoded_string, cipher):
        """
        `process_decode()` stores the result if the encoding is valid
        after checks from `contains_replacement_char()` and
        prints the output if it isn't an API call
        """
        encoding_ciphers = self.encoding_ciphers
        decoded_strings = self.decoded_strings

        if len(decoded_string) < 3: return
        if not self.contains_replacement_char(decoded_string):
            # don't repeat `base64url` when `base64` has already passed and it's not a URL
            if cipher == 'Base64' and '://' not in decoded_string:
                self.b64_once = True
                
            if self.b64_once and (cipher == 'Base64URL'):
                return
            
            # append decoded_strings to the respective lists
            encoding_ciphers.append(cipher)
            decoded_strings.append(decoded_string)

            if not self.api_call:
                if self.image_mode_call:
                    print(
                        colored('\n[-] Attempting Base: ', 'yellow') +
                        colored(self.encoded_crypto, 'red')
                    )

                print(
                    colored('\n[>] Decoding as {}: '.format(cipher), 'blue') +
                    colored(decoded_string, 'green')
                )

    def decode_crypto(self):
        encoded_crypto = self.encoded_crypto
        process_decode = self.process_decode

        # decoding as base16
        try:
            process_decode(
                base64.b16decode(encoded_crypto, casefold=False).decode('utf-8', 'replace'),
                'Base16'
            )
        except Exception as _: pass

        # decoding as base32
        try:
            process_decode(
                base64.b32decode(
                    encoded_crypto, casefold=False, map01=None
                ).decode('utf-8', 'replace'),
                'Base32'
            )
            self.b32_once = True
        except Exception as _: pass

        # decoding as base32 (RFC 3548)
        if not self.b32_once:
            try:
                """
                Base32 charset can differ based on their spec, this requires stripping
                the padding or changing charsets to get the correct decoded_strings.
                By default this `base32` implementation follows the RFC 3548 spec.
                """
                temp_clean_crypto = str.encode(encoded_crypto.replace('=', ''))
                process_decode(
                    base32.decode(temp_clean_crypto).decode('utf-8', 'replace'),
                    'Base32'
                )
            except Exception as _: pass                

        # decoding as base36
        try:
            process_decode(
                base36.dumps(int(encoded_crypto)),
                'Base36'
            )
        except Exception as _: pass

        # decoding as base45
        try:
            process_decode(
                base45.b45decode(encoded_crypto).decode('utf-8', 'replace'),
                'Base45'
            )
        except Exception as _: pass

        # decoding as base58
        try:
            process_decode(
                base58.b58decode(encoded_crypto.encode()).decode('utf-8', 'replace'),
                'Base58'
            )
        except Exception as _: pass

        # decoding as base62
        try:
            process_decode(
                base62.decodebytes(encoded_crypto).decode('utf-8', 'replace'),
                'Base62'
            )
        except Exception as _: pass

        # decoding as base64
        try:
            process_decode(
                base64.b64decode(encoded_crypto).decode('utf-8', 'replace'),
                'Base64'
            )
        except Exception as _: pass

        # decoding as base64url
        try:
            process_decode(
                base64.urlsafe_b64decode(
                    encoded_crypto + '=' * (4 - len(encoded_crypto) % 4)
                ).decode('utf-8', 'replace'),
                'Base64URL'
            )
        except Exception as _: pass

        # decoding as base85
        try:
            process_decode(
                base64.b85decode(encoded_crypto).decode('utf-8', 'replace'),
                'Base85'
            )
        except Exception as _: pass

        # decoding as ascii85
        try:
            process_decode(
                base64.a85decode(encoded_crypto).decode('utf-8', 'replace'),
                'Ascii85'
            )
        except Exception as _: pass

        # decoding as base91
        try:
            process_decode(
                base91.decode(encoded_crypto).decode('utf-8', 'replace'),
                'Base91'
            )
        except Exception as _: pass

        # decoding as base92
        try:
            process_decode(
                base92.decode(encoded_crypto),
                'Base92'
            )
        except Exception as _: pass

        # decoding as base100 lol why??!!
        try:
            process_decode(
                base100.decode(encoded_crypto).decode(),
                'Base100'
            )
        except Exception as _: pass

        # decoding as hex
        try:
            process_decode(
                hexCode.decode(encoded_crypto),
                'Hex'
            )
        except Exception as _: pass

        # decoding as Morse code
        try:
            process_decode(
                morse.decode(encoded_crypto),
                'Morse'
            )
        except Exception as _: pass

        # decoding as cvecode
        try:
            process_decode(
                cvecode.decode(encoded_crypto),
                'Cvecode'
            )
        except Exception as _: pass

        # decoding as XXencode
        try:
            process_decode(
                xxencode.decode(encoded_crypto),
                'XXencode'
            )
        except Exception as _: pass

        # decoding as Buddha
        try:
            process_decode(
                buddha.decode(encoded_crypto),
                'Buddha'
            )
        except Exception as _: pass

        # decoding as UUencode
        # decoding as PPencode
        # decoding as AAencode
        # decoding as JJencode
        # decoding as JSFuck
        # decoding as BrainFuck
        # decoding as Korea
        # decoding as BubbleBabble
        # decoding as Baconian
        # decoding as A1z26

        # decoding as rot13
        try:
            process_decode(
                rot13.decode(encoded_crypto),
                'Rot13'
            )
        except Exception as _: pass

        # decoding as rot47
        # decoding as rot3000
        # decoding as Atbash 


        # decoding as Cipher needs key, not magic mode

