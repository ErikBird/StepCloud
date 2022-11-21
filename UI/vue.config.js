module.exports = {
    productionSourceMap: false,
    "transpileDependencies": [
        "vuetify"
    ],
    pages: {
        index: {
            // entry for the page
            entry: 'src/main.js',
            // the source template
            template: 'public/index.html',
            // output as dist/index.html
            filename: 'index.html',
            // when using title option,
            // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
            title: 'Index Page',
            // chunks to include on this page, by default includes
            // extracted common chunks and vendor chunks.
            chunks: ['chunk-vendors', 'chunk-common', 'index']
        },
    },
    pluginOptions: {
        i18n: {
            locale: 'de',
            fallbackLocale: 'en',
            localeDir: 'locales',
            enableInSFC: false
        },
        electronBuilder: {
            nodeIntegration: true,
            outputDir: 'electron-builder-output-dir',
            builderOptions: {
                appId: "de.stepcloud.app",
                productName: 'stepcloud',
                icon: "./public/icon.png",
                extraResources: [
                    "build/**/*"
                ],
                artifactName: "${productName}-${version}.${ext}",
                win: {
                    target: "nsis",
                    verifyUpdateCodeSignature: false
                },
                linux: {
                    target: [
                        "AppImage"
                    ]
                },
                publish:
                    [
                        {
                            provider: "github",
                            publishAutoUpdate: true,
                            repo: "DesktopClient",
                            owner: "ErikBird",
                            private: true
                        }
                    ]
            }
        }
    }
}
