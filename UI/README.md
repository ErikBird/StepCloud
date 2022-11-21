# lithohub-desktop

#### Automatic release

You can generate a new version release with this command:

```
npm run release
```

It automatically updates the CHANGELOG.md file.

## Build Windows and Linux in parallel on Linux (Wine need to be installed)

```
 npm run electron:build -- --linux deb --win nsis
```

## Serve Electron App

```
vue-cli-service electron:serve
```

## Build Electron App

```
vue-cli-service electron:build
```

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Generate Icons

```
npm run electron:generate-icons
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

### Electron Gitlab Integration

https://gist.github.com/m3doune/293832c8158528738c04359a1e1e40bd

### To Resolve any error by Segmentation Faults

```
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Device Image Assets

Since the path for the image assets are stored in the database, and then received by an api call, they can not be
preloaded.
Therefore, the device images have to be stored in the public folder, which is always included during build.
One can read further about the issue here: https://cli.vuejs.org/guide/html-and-static-assets.html#the-public-folde
