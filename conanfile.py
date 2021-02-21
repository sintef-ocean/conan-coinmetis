from conans import AutoToolsBuildEnvironment, ConanFile, tools
from contextlib import contextmanager
from os import path, unlink


class CoinMetisConan(ConanFile):
    name = "coinmetis"
    version = "4.0.3"
    license = ("https://github.com/CIBC-Internal/metis-4.0.3/blob/master/LICENSE",)
    author = "SINTEF Ocean"
    url = "https://github.com/sintef-ocean/conan-coinmetis"
    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/metis/overview"
    description =\
        "METIS is a set of serial programs for partitioning graphs, "\
        "partitioning finite element meshes, and producing fill " \
        "reducing orderings for sparse matrices."
    topics = ("Matrix ordering", "Partitioning graphs", "COIN-OR")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}

    _coin_helper = "ThirdParty-Metis"
    _coin_helper_branch = "stable/2.0"
    _autotools = None

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools

        self._autotools = AutoToolsBuildEnvironment(
            self,
            win_bash=tools.os_info.is_windows)
        self._autotools.libs = []

        if self.settings.compiler == "Visual Studio":
            self._autotools.flags.append("-FS")

        yes_no = lambda v: "yes" if v else "no"
        configure_args = [
            "--enable-shared={}".format(yes_no(self.options.shared)),
            "--enable-static={}".format(yes_no(not self.options.shared)),
        ]

        if self.settings.compiler == "Visual Studio":
            configure_args.append(
                "--enable-msvc={}".format(self.settings.compiler.runtime))

        self._autotools.configure(args=configure_args)
        return self._autotools

    @contextmanager
    def _build_context(self):
        if self.settings.compiler == "Visual Studio":
            with tools.vcvars(self.settings):
                env = {
                    "CC": "{} cl -nologo".format(tools.unix_path(
                        self.deps_user_info["automake"].compile)),
                    "CXX": "{} cl -nologo".format(tools.unix_path(
                        self.deps_user_info["automake"].compile)),
                    "LD": "link -nologo",
                    "AR": "{} lib".format(tools.unix_path(
                        self.deps_user_info["automake"].ar_lib)),
                }
                with tools.environment_append(env):
                    yield
        else:
            yield

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requirements(self):
        if tools.os_info.is_windows and not tools.get_env("CONAN_BASH_PATH"):
            self.build_requires("msys2/20200517")
        if self.settings.compiler == "Visual Studio":
            self.build_requires("automake/[>=1.16.3]")

    def source(self):
        _git = tools.Git()
        _git.clone("https://github.com/coin-or-tools/{}.git"
                   .format(self._coin_helper),
                   branch=self._coin_helper_branch,
                   shallow=True)

        self.run("./get.Metis", win_bash=tools.os_info.is_windows)

    def build(self):
        with self._build_context():
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        with self._build_context():
            autotools = self._configure_autotools()
            autotools.install()

        tools.rmdir(path.join(self.package_folder, "lib", "pkgconfig"))
        unlink(path.join(self.package_folder, "lib", "libcoinmetis.la"))
        self.copy("INSTALL.Metis", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = ["coinmetis"]
        # TODO: The dll is named coinmetis-2, should I be worried?
        self.cpp_info.includedirs = [path.join("include", "coin-or", "metis")]

    def imports(self):
        self.copy("license*", dst="licenses", folder=True, ignore_case=True)
