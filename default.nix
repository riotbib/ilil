{ config, lib, pkgs, ... }:

with lib;

let
    ilil = pkgs.python3.pkgs.buildPythonApplication {
      pname = "ilil";
      version = "unstable-20200819p";

      src = lib.cleanSource ./.; 

      propagatedBuildInputs = with pkgs.python3Packages; [ bottle pillow numpy toml ];

      meta = {
        homepage = https://github.com/riotbib/ilil;
        description = "ilil is an insta-like image log. :^)";
        license = lib.licenses.gpl3;
      };

      installPhase = ''
        mkdir -p $out/bin
        cp $src/ilil.py $out/bin
        cp -r $src/views $out/bin 
      '';

    };

    ilil-uid = 9161;

    ililConfig = pkgs.writeText "config.toml" ''
        title = '${cfg.title}'

        [owner]
        name = '${cfg.ownerName}'
        mail = '${cfg.ownerMail}'
        description = '${cfg.ownerDescription}'

        [server]
        host = '${cfg.serverHost}'
        port = '${toString cfg.serverPort}'
        password = '${cfg.serverPassword}'
        itemsPerPage = '${toString cfg.serverItemsPerPage}'
        path = '${cfg.serverPath}'
    '';

    cfg = config.services.ilil;

in {
  options.services.ilil = {
    enable = mkEnableOption "ilil";

    title = mkOption {
      default = "ilil";
      type = types.str;
      description = "Title of the image log";
    };

    ownerName = mkOption {
      type = types.str;
      description = "Name of the owner";
    };

    ownerMail = mkOption {
      type = types.str;
      description = "Mail address of the owner";
    };

    ownerDescription = mkOption {
      default = "This is an insta-like image log.";
      type = types.str;
      description = "Description of the log";
    };

    serverHost = mkOption {
      default = "localhost";
      type = types.str;
      description = "Server host to use";
    };

    serverPort = mkOption {
      default = 80;
      type = types.port;
      description = "Server port to use";
    };

    serverPassword = mkOption {
      default = "hackme";
      type = types.str;
      description = "Server password to use";
    };

    serverItemsPerPage = mkOption {
      default = 100;
      type = types.ints.unsigned;
      description = "Items per page to display";
    };

    serverPath = mkOption {
      default = "/var/www/ilil";
      type = types.path;
      description = "Directory for ilil's store";
    };

  };

  config = mkIf cfg.enable {
    environment.systemPackages = [ ilil ];

    systemd.services.ilil = {
      description = "ilil";

      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];

      serviceConfig = {
        ExecStart = ''
          ${ilil}/bin/ilil.py \
            -c ${ililConfig} \
            -p ${cfg.serverPath}
        '';

        Type = "simple";

        User = "ilil";
        Group = "ilil";
      };
    };

    users.users.ilil = {
      group = "ilil";
      home = cfg.serverPath;
      createHome = true;
      uid = ilil-uid;
    };

    users.groups.ilil.gid = ilil-uid;

  };

}
