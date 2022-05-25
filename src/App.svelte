<script>
    import Header from "./Header.svelte";

    const repo_path = "https://raw.githubusercontent.com/phuang1024/pianoray/master/"
    const img1 = repo_path + "examples/renders/clementi.jpg"
</script>

<Header/>

<div class="main">
    <div class="alltext">
        <h1>PianoRay</h1>
        <h3 style="text-align: center">A free and open source piano visualizer.</h3>
    </div>
</div>

<style>
	h1, h2, h3, p {
		color: #dddddd;
        font-family: Ubuntu;
		font-weight: 350;
	}

    h1 {
		font-size: 3em;
        text-align: center;
		text-transform: uppercase;
    }

    h2 {
        font-size: 2.3em;
    }

    h3 {
        font-size: 1.6em;
    }

    p {
        font-size: 1em;
    }

    img {
        opacity: 0.5;
        width: 100%;
    }

    .main {
        background-image: url(../clementi.jpg);
        display: block;
        min-height: 100%;
    }

    .alltext {
        padding: 2em;
        padding-top: 1em;
    }
</style>
