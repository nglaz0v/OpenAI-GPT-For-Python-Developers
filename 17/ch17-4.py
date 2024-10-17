import os
import openai
import random
import time


def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")


init_api()

artists = ["Mohammed Amin","Dorothea Lange","Yousuf Karsh ","Helmut Newton","Diane Arbus","Eric Lafforgue","Annie Leibovitz","Lee Jeffries","Steve McCurry","Dmitry Ageev","Rosie Matheson","Nancy Goldin","David Lachapelle","Peter Lindbergh","Robert Mapplethorpe","David Bailey","Terry Richardson","Martin Schoeller","Julia Margaret Cameron","George Hurrell","Ansel Adams","Dorothea Lange","Edward Weston","Elliott Erwitt","Henri Cartier-Bresson","Robert Capa","W. Eugene Smith","Garry Winogrand","Diane Arbus","Robert Frank","Walker Evans","Robert Mapplethorpe","Pablo Picasso","Vincent Van Gogh","Claude Monet","Edvard Munch","Salvador Dali","Edgar Degas","Paul Cezanne","Rene Magritte","Sonia Delaunay","Zeng Fanzhi","Vitto Ngai","Yoji Shinkawa","J.M.W. Turner","Gerald Brom","Jack Kirby","Pre-Raphaelite","Alphonse Mucha","Caspar David Friedrich","William Blake","William Morris","Albrecht Durer","Raphael Sanzio","Michelangelo Buonarroti","Leonardo Da Vinci","Rene Magritte",]

art_styles = ["Art Nouveau", "Impressionism", "Abstract Expressionism", "Orphism", "Neoclassicism", "Cubism", "Fauvism", "Surrealism", "Expressionism", "Dadaism", "Pop Art", "Minimalism", "Postmodernism", "Futurism", "Art Deco", "Early Renaissance", "Religious Art", "Chinese Art", "Baroque", "Art Nouveau", "Impressionism", "Abstract Expressionism", "Orphism", "Neoclassicism", "Cubism", "Fauvism", "Surrealism", "Expressionism", "Dadaism", "Pop Art", "Minimalism", "Postmodernism", "Futurism", "Art Deco", "Early Renaissance", "Religious Art", "Chinese Art", "Baroque", "3D sculpture", "Comic book", "Sketch drawing", "Old photograph", "Modern photograph", "Portrait", "Risograph", "Oil painting", "Graffiti", "Watercolor", "Cyberpunk", "Synthwave", "Gouache", "Pencil drawing (detailed, hyper-detailed, very realistic)", "Pastel drawing", "Ink drawing", "Vector", "Pixel art", "Video game", "Anime", "Manga", "Cartoon", "Illustration", "Poster", "Typography", "Logo", "Branding", "Etching", "Woodcut", "Political cartoon", "Newspaper", "Coloring sheet", "Field journal line art", "Street art", "Airbrush", "Crayon", "Child's drawing", "Acrylic on canvas", "Pencil drawing (colored, detailed)", "Ukiyo-e", "Chinese watercolor", "Pastels", "Corporate Memphis design", "Collage (photo, magazine)", "Watercolor & pen", "Screen printing", "Low poly", "Layered paper", "Sticker illustration", "Storybook", "Blueprint", "Patent drawing", "Architectural drawing", "Botanical illustration", "Cutaway", "Mythological map", "Voynich manuscript", "IKEA manual", "Scientific diagram", "Instruction manual","Voroni diagram", "Isometric 3D", "Fabric pattern", "Tattoo", "Scratch art", "Mandala", "Mosaic", "Black velvet (Edgar Leeteg)", "Character reference sheet", "Vintage Disney", "Pixar", "1970s grainy vintage illustration", "Studio Ghibli", "1980s cartoon", "1960s cartoon",]

vibes = ["light", "peaceful", "calm", "serene", "tranquil", "soothing", "relaxed", "placid", "comforting", "cosy", "tranquil", "quiet", "pastel", "delicate", "graceful", "subtle", "balmy", "mild", "ethereal", "elegant", "tender", "soft", "light", "muted", "bleak", "funereal", "somber", "melancholic", "mournful", "gloomy", "dismal", "sad", "pale", "washed-out", "desaturated", "grey", "subdued", "dull", "dreary", "depressing", "weary", "tired", "dark", "ominous", "threatening", "haunting", "forbidding", "gloomy", "stormy", "doom", "apocalyptic", "sinister", "shadowy", "ghostly", "unnerving", "harrowing", "dreadful", "frightful", "shocking", "terror", "hideous", "ghastly", "terrifying", "bright", "vibrant", "dynamic", "spirited", "vivid", "lively","energetic", "colorful", "joyful", "romantic", "expressive", "bright", "rich", "kaleidoscopic", "psychedelic", "saturated", "ecstatic", "brash", "exciting", "passionate", "hot", "from Dancer in the Dark movie ", "from Howl's Moving Castle movie ", "from Coraline movie ", "from Hanna movie ", "from Inception movie ", "from Thor movie ", "from The Lion King movie ", "from Rosemary's Baby movie ", "from Ocean's Eleven movie ", "from Lovely to Look At movie ", "from Eve's Bayou movie ", "from Tommy movie ", "from Chocolat movie ", "from The Godfather movie ", "from Kill Bill movie ", "from The Lord of the Rings movie ", "from Legend movie ", "from The Abominable Dr. Phibes movie ", "from The Shining movie ", "from Pan's Labyrinth movie ", "from Blade Runner movie ", "from Lady in the Water movie ", "from The Wizard of Oz movie",]

colors = ["Blue", "Red", "Green", "Yellow", "Purple", "Pink", "Orange", "Black", "White", "Gray", "Red and Green", "Yellow and Purple", "Orange and Blue", "Black and White", "Pink and Teal", "Brown and Lime", "Maroon and Violet", "Silver and Crimson", "Beige and Fuchsia", "Gold and Azure", "Cyan and Magenta", "Lime and Maroon and Violet", "Crimson and Silver and Gold", "Azure and Beige and Fuchsia", "Magenta and Cyanand Teal", "Pink and Teal and Lime", "Yellow and Purple and Maroon", "Orange and Blue and Violet", "Black and White and Silver", "Fade to Black", "Fade to White", "Fade to Gray", "Fade to Red", "Fade to Green", "Fade to Blue", "Fade to Yellow", "Fade to Purple", "Fade to Pink", "Fade to Orange", "Gradient of Red and Green", "Gradient of Yellow and Purple", "Gradient of Orange and Blue", "Gradient of Black and White", "Gradient of Pink and Teal", "Gradient of Brown and Lime", "Gradient of Maroon and Violet", "Gradient of Silver and Crimson", "Gradient of Beige and Fuchsia", "Gradient of Gold and Azure", "Gradient of Cyan and Magenta",]

resolution = ["2 bit colors", "4 bit colors", "8 bit colors", "16 bit colors", "24 bit colors", "4k resolution", "HDR", "8K  resolution", "a million colors", "a billion colors",]

angles = ["Extreme close-up","close-up","medium shot","long shot","extreme long shot","high angle","overhead view","aerial view","tilted frame","dutch angle","over-the-shoulder shot","drone view","panning shot","tracking shot","dolly shot","zoom shot", "handheld shot","crane shot","low angle","reverse angle","point-of-view shot","split screen","freeze frame","flashback","flash forward","jump cut","fade in","fade out",]

lens = ["high-resolution microscopy", "microscopy", "macro lens", "pinhole lens", "knolling", "first person view", "wide angle lens", "lens distortion", "ultra-wide angle lens", "fisheye lens", "telephoto lens", "panorama", "360 panorama", "tilt-shift lens", "telescope lens", "lens flare", "Aperture: f/5.6, Shutter Speed: 1/250s, ISO: 400,  Landscape photography, high-quality DSLR", "Aperture: f/8, Shutter Speed: 1/60s, ISO: 800, Street photography, low light conditions", "Aperture: f/11, Shutter Speed: 1/1000s, ISO: 1600, Sports photography, fast shutter speed", "Aperture: f/16, Shutter Speed: 2s, ISO: 100, Night photography, long exposure", "Aperture: f/2.8, Shutter Speed: 1/500s, ISO: 1600, Wildlife photography, high sensitivity, high ISO", "Aperture: f/4, Shutter Speed: 1/60s, ISO: 100, Portrait photography, shallow depth of field", "Aperture: f/5.6, Shutter Speed: 1/60s, ISO: 100, Macro photography, close-up shots", "Aperture: f/8, Shutter Speed: 1/15s, ISO: 100, Fine art photography, Kodak Gold 200 film color, 35mm", "Aperture: f/11, Shutter Speed: 4s, ISO: 200, Architectural photography, slow shutter speed, long exposure.",]

light = ["Warm lighting", "Side lighting", "High-key lighting", "fluorescent lighting", "Harsh flash lighting", "Low-key lighting", "Flat lighting", "Even lighting", "Ambient lighting", "Colorful lighting", "Soft light", "Hard light", "Diffused light", "Direct light", "Indirect light", "Studio lighting", "Red and green lighting", "Flash photography", "Natural lighting", "Backlighting", "Edge lighting", "Cold", "Backlit", "Glow", "Neutral white", "High-contrast", "Lamp light", "Fireworks", "2700K light", "4800K light", "6500K light",]

filter = ["Kodachrome", "Autochrome", "Lomography", "Polaroid", "Instax", "Cameraphone", "CCTV", "Disposable camera", "Daguerrotype", "Camera obscura", "Double exposure", "Cyanotype", "Black and white", "Tri-X 400TX", "Infrared photography", "Bleach bypass", "Contact sheet", "Colour splash", "Solarised", "Anaglyph", "Instagram Clarendon filter", "Instagram Juno filter", "Instagram Ludwig filter", "Instagram Lark filter", "Instagram Gingham filter", "Instagram Lo-fi filter", "Instagram X-Pro II filter", "Instagram Aden filter", "Instagram Perpetua filter", "Instagram Reyes filter", "Instagram Slumber filter" ]

lists = [
    colors,
    resolution,
    angles,
    lens,
    light,
    filter
]

user_prompts = [
    "Happy Darth Vader smiling and waving at tourists in a museum of Star Wars memorabilia.",
    "Darth Vader rapping with 2Pac.",
    "Darth Vader playing the piano.",
    "Darth Vader playing the guitar.",
    "Darth Vader eating sushi.",
    "Darth Vader drinking a glass of milk.",
]

n = 5

for user_prompt in user_prompts:
    print("Генерация изображения по запросу: " + user_prompt)
    for i in range(n):
        customizations = ""
        for j in range(len(lists)):
            list = lists[j]
            choose_or_not = random.randint(0, 1)
            if choose_or_not == 1:
                customizations += random.choice(list) + ", "

        kwargs = {
            "prompt": user_prompt + ", " + customizations,
            "n": n,
        }

        print("Генерация изображения номер: " + str(i+1) + ". Используем запрос: " + user_prompt + ", " + customizations)
        im = openai.Image.create(**kwargs)
        print(im.data[i].url)
        print("\n")
        time.sleep(1)
    print("Завершена генерация изображений по запросу: " + user_prompt)
